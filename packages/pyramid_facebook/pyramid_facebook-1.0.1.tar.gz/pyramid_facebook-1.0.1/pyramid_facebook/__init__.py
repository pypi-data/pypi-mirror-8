# -*- coding: utf-8 -*-
import logging


log = logging.getLogger(__name__)


def includeme(config):
    settings = config.registry.settings

    path = '/%s' % settings['facebook.namespace']

    config.include('pyramid_mako')
    config.include('pyramid_facebook.predicates', route_prefix=path)
    config.include('pyramid_facebook.security', route_prefix=path)
    config.include('pyramid_facebook.auth', route_prefix=path)
    config.include('pyramid_facebook.canvas', route_prefix=path)
    config.include('pyramid_facebook.utility', route_prefix=path)
    # XXX make inclusion of old credits conditional?
    config.include('pyramid_facebook.credits', route_prefix=path)
    config.include('pyramid_facebook.real_time', route_prefix=path)
    config.include('pyramid_facebook.opengraph', route_prefix=path)
    config.include('pyramid_facebook.payments', route_prefix=path)
    config.commit()
