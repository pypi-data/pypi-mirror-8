# -*- coding: utf-8 -*-
from pyramid.decorator import reify

from pyramid_facebook.lib import Base


class OauthAccept(Base):
    "Event sent when a user accepts app authentication."


class OauthDeny(Base):
    "Event sent when a user denies app authentication."


class DisputedOrder(Base):
    "Event sent when a user disputes an order."


class RefundedOrder(Base):
    "Event sent when a user got refunded for an order."


class PlacedItemOrder(Base):
    "Event sent when a user placed an item order."


class CanceledOrder(Base):
    "Event sent when an order failed because of an internal error."


class EarnedCurrencyOrder(Base):
    "Event sent when a user placed an currency order."


class ChangeNotification(Base):
    """Event sent when Facebook notifies about a real-time update.

    For more info, read doc on `Facebook Documentation
    <https://developers.facebook.com/docs/reference/api/realtime/>`_.
    """
    def __init__(self, context, request):
        super(ChangeNotification, self).__init__(context, request)
        self.object = self.json_body['object']

    @reify
    def json_body(self):
        """:returns: Request body as a dict. Raised an error if body is json
            decoding fails."""
        return self.request.json_body


class UserSignedRequestParsed(Base):
    """Event sent each time a signed request with user information is
    successfully parsed.
    """


class CanvasRequested(Base):
    """Event sent when an identified user requests the application canvas.
    """


# events for new local currency payments

class OrderReceived(object):
    """An order for a local currency payment was received"""

    def __init__(self, request, payment):
        self.request = request
        self.payment = payment


class OrderProcessingError(object):
    """An exception happened when notifying OrderReceived."""

    def __init__(self, request, payment):
        self.request = request
        self.payment = payment


class OrderRefunded(object):
    """A disputed payment was refunded."""

    def __init__(self, request, payment):
        self.request = request
        self.payment = payment
