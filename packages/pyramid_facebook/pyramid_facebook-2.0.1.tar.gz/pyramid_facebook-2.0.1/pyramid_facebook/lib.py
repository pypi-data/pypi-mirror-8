# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
import json


js_redirect_tpl = """<html>
  <body>
    <script>
      window.top.location = "%(location)s";
    </script>
  </body>
</html>"""


# TODO mostly useless, delete

class Base(object):
    "Base class for views and events"
    def __init__(self, context, request):
        self.context = context
        self.request = request


def _base64_url_encode(inp):
    """ Facebook base64 decoder based on `Sunil Arora's blog post
    <http://sunilarora.org/parsing-signedrequest-parameter-in-python-bas>`_.

    :param inp: input `str` to be encoded
    :return: `base64` encoded utf8 unicode data
    """
    return unicode(base64.b64encode(inp, '-_').strip('=').encode('utf8'))


# TODO deprecate in favor of facepy

def encrypt_signed_request(secret_key, data):
    """Encrypts data the way facebook does for permit testing. Adds algorithm
    key to dict.

    :param secret_key: Facebook application' secret key.
    :param data: a dictionary of data to sign.
    :return: Signed request as defined by `Facebook documentation
             <http://developers.facebook.com/docs/authentication/
             signed_request/>`_

    """
    data = data.copy()
    data.update(algorithm='HMAC-SHA256')

    payload = _base64_url_encode(json.dumps(data)).encode('utf8')
    signature = _base64_url_encode(
        hmac.new(
            secret_key.encode('utf8'),
            msg=payload.encode('utf8'),
            digestmod=hashlib.sha256
            ).digest()
        )
    return '%s.%s' % (signature, payload)
