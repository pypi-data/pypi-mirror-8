# -*- coding: utf-8 -*-
import logging
import urllib

from pyramid.events import NewResponse, subscriber
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPForbidden

from pyramid_facebook.events import CanvasRequested
from pyramid_facebook.lib import js_redirect_tpl
from pyramid_facebook.security import ViewCanvas, SignedRequestContext

log = logging.getLogger(__name__)


def includeme(config):
    """Adds routes related to facebook canvas.

    Routes added:

    * ``facebook_canvas`` associated to url ``/{namespace}/`` that musts be
      configured as canvas callback url in facebook application settings.

    * ``facebook_canvas_oauth`` associated to url ``/{namespace}/oauth`` for
      authentication.

    """
    log.debug('Adding route "facebook_canvas".')
    config.include('pyramid_facebook.auth')
    config.include('pyramid_facebook.security')
    config.include('pyramid_facebook.predicates')
    config.add_route(
        'facebook_canvas',
        '/',
        request_method='POST',
        request_param='signed_request',
        factory='pyramid_facebook.security.SignedRequestContext',
        )
    config.add_route(
        'redirect_to_app',
        '/',
        request_method='GET'
        )
    config.scan(package='pyramid_facebook.canvas')


class facebook_canvas(view_config):
    """Decorator that registers a view for the ``facebook_canvas`` route
    with the ``view_canvas`` permission.

    Accepts same arguments as :class:`~pyramid.view.view_config`::

        @facebook_canvas(renderer='canvas.mako')
        def canvas(context, request):
            return {
                'title': 'A great Facebook Game'
                }
    """
    def __init__(self, **kwargs):
        config = kwargs.copy()
        config.update({
            'permission': ViewCanvas,
            'route_name': 'facebook_canvas',
            })
        super(facebook_canvas, self).__init__(**config)


class facebook_install_canvas(view_config):
    """Decorator that registers a view for the ``facebook_canvas`` route
    with context ``~pyramid.httpexceptions.HTTPForbidden``.

    Accepts same arguments as :class:`~pyramid.view.view_config`::

        @facebook_install_canvas(renderer='install.mako')
        def canvas(context, request):
            return {
                'title': 'A great Facebook Game'
                }
    """
    def __init__(self, **kwargs):
        config = kwargs.copy()
        config.update({
            'context': HTTPForbidden,
            'route_name': 'facebook_canvas',
            })
        super(facebook_install_canvas, self).__init__(**config)


@facebook_install_canvas()
def prompt_authorize(context, request):
    """User is not logged in, view prompts user to authorize app:

    * User is not logged in
    * User is on apps.facebook.com/{namespace}
    """
    settings = request.registry.settings
    path = request.route_path('facebook_canvas_oauth')
    query_string = request.GET.copy()
    query_string.pop('code', None)
    redirect_uri = urllib.quote_plus("%s://apps.facebook.com%s?%s" % (
        request.scheme,
        path,
        urllib.urlencode(query_string),
        ))

    values = (
        "https://www.facebook.com",
        settings['facebook.app_id'],
        redirect_uri,
        settings['facebook.scope'].replace(' ', ''),
    )
    url = ("%s/dialog/oauth?client_id=%s&display=page&redirect_uri=%s"
           "&response_type=code&scope=%s&canvas=1" % values)
    log.debug('Prompt authorize, redirecting user on %s', url)
    return Response(js_redirect_tpl % {'location': url})


@facebook_canvas()
def canvas(context, request):
    """When users are logged in, they are authorized to view canvas.

    This view raises :py:exc:`exceptions.NotImplementedError`
    """
    log.error(
        'No facebook canvas configured: use %s decorator.',
        facebook_canvas
        )
    raise NotImplementedError()


@view_config(route_name='redirect_to_app')
def redirect_to_app(context, request):
    """Attempting to directly access the canvas through a GET request
    redirects the user to the actual Facebook app.
    """
    url = "%s://apps.facebook.com/%s" % (
        request.scheme,
        request.registry.settings['facebook.namespace'],
        )
    return Response(js_redirect_tpl % {'location': url})


@subscriber(
    NewResponse,
    matched_route='facebook_canvas',
    expected_context=SignedRequestContext,
    )
def on_canvas(event):
    try:
        event.request.registry.notify(CanvasRequested(event.request.context,
                                                      event.request))
    except Exception:
        log.exception('CanvasRequested subscriber fail.')
