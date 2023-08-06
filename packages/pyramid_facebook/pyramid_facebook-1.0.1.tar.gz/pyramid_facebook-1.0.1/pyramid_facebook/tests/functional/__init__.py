# -*- coding: utf-8 -*-
from __future__ import absolute_import

import unittest
import webtest

from pyramid.config import Configurator
from pyramid.authentication import CallbackAuthenticationPolicy
from pyramid.security import IAuthorizationPolicy, IAuthenticationPolicy

from zope.interface import implementer


@implementer(IAuthenticationPolicy)
class DummyAuthenticationPolicy(CallbackAuthenticationPolicy):
    def unauthenticated_userid(self, request):
        return None


@implementer(IAuthorizationPolicy)
class PermissiveAuthorizationPolicy(object):
    def permits(self, context, principals, permission):
        return True


class TestView(unittest.TestCase):
    _permissive_app = None

    @property
    def config(self):
        if not hasattr(self, '_config'):
            from pyramid_facebook import includeme
            from pyramid_facebook.tests import conf
            self._config = Configurator(settings=conf)
            self._config.include(includeme)
            self.addCleanup(delattr, self, '_config')
        return self._config

    @property
    def app(self):
        if not hasattr(self, '_app'):
            self._app = webtest.TestApp(self.config.make_wsgi_app())
            self.addCleanup(delattr, self, '_app')
        return self._app

    @property
    def permissive_app(self):
        if TestView._permissive_app is None:
            from pyramid_facebook import (
                auth,
                canvas,
                credits,
                real_time,
                predicates,
                )
            from pyramid_facebook.tests import conf
            namespace = conf['facebook.namespace']
            config = Configurator(settings=conf)
            config.include(predicates, route_prefix=namespace)
            config.include(auth, route_prefix=namespace)
            config.include(canvas, route_prefix=namespace)
            config.include(credits, route_prefix=namespace)
            config.include(real_time, route_prefix=namespace)
            config.set_authentication_policy(DummyAuthenticationPolicy())
            config.set_authorization_policy(PermissiveAuthorizationPolicy())
            config.commit()
            TestView._permissive_app = webtest.TestApp(config.make_wsgi_app())
        return TestView._permissive_app
