================
pyramid_facebook
================

.. image:: https://drone.io/bitbucket.org/Ludia/pyramid_facebook/status.png
   :target: https://drone.io/bitbucket.org/Ludia/pyramid_facebook

.. image:: https://pypip.in/d/pyramid_facebook/badge.png
   :target: https://crate.io/packages/pyramid_facebook/

Provides simple pyramid routes/views for facebook canvas application.

Some documentation on https://pyramid-facebook.readthedocs.org/en/latest/

Configuration
=============

#. Create facebook application on https://developers.facebook.com/apps

#. Add facebook settings in .ini file under application section and fill with
   facebook application parameters:

   .. code-block:: ini

         facebook.app_id =
         facebook.secret_key =
         facebook.namespace =
         facebook.scope =

#. In the app settings on https://developers.facebook.com/apps, set callbak url
   to point to `http://127.0.0.1:6543/[facebook app namespace]/`

#. Include ``pyramid_facebook`` in your config:

   .. code-block:: python

         config.include('pyramid_facebook')
         config.scan()

#. Define your facebook canvas view:

   .. code-block:: python

         from pyramid_facebook.canvas import facebook_canvas

         @facebook_canvas()
         def canvas(context, request):
            # canvas is available only to users who accepted facebook permission
            # defined in setting['facebook.scope'].
            # context.facebook_data dict contains signed_request content.
            # i.e.:
            # user_id = context.facebook["user_id"]
            return Response('Hello Facebok World')

#. Browse to your app on `http://apps.facebook.com/[app namespace]`
