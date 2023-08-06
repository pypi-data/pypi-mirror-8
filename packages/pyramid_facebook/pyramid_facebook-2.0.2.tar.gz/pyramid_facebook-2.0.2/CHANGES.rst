Changelog
=========

2.0.2 (2014-12-17)
------------------

* Add a test configuration in ``pyramid_facebook.tests`` which mocks facepy
  graph api object. To use it in functionnal tests:
  ``config.include('pyramid_facebook.tests')`` when configuring test app.

2.0.1 (2014-11-25)
------------------

* Upgrade to facebook graph api v2

1.0.1 (2014-11-25)
------------------

* Add Facebook payment event type for refunded orders.

0.6.7 (2014-08-26)
------------------

* Remove constraint on ``pyramid_contextauth`` version requirement.
* Add ``pyramid_mako`` as required dependency.

0.6.6 (2014-05-05)
------------------

* Improve request property ``request.graph_api``
* Add request property ``request.fb_app_token``

0.6.5 (2014-04-23)
------------------

* 2014-04-23 - Facebook real time payment fails and logging code raises a
  KeyError.

0.6.4 (2014-03-26)
------------------

0.6.3 (2014-03-25)
------------------

* Fix doc and rst file for pypi.

0.6.2 (2014-03-25)
------------------

* Remove `authentication_policy` decorator in favor of `config.register_authentication_policy`.

0.6.1 (2014-03-24)
------------------

* Update dependency to pyramid_contextauth >= 0.5

0.5.324
-------

* Add a `GraphAPI` utility lazily instantiated with the application token.
* Add attribute `ChangeNotification.object` event.
* Event `OrderReceived` is notified when receiving a real-time payment update
* Add `pyramid_facebook.tests.integration.test_payments` used in
  `pyramid_facebook.tests.functional.test_payments`

Breaking Changes
````````````````

* Rename `OrderCreated` for `OrderReceived`

   * Can be sent multiple times for the same order with same or different
     status

* Rename `OrderCreationError` for `OrderProcessingError`

0.4.317
-------

* Added pfacebook-real-time command to update real time subscriptions.
* Breaking changes: namespace is now added by the framework in opengraph URLs.


0.2.246
-------

* Reusable view and template for OpenGraph objects.
* Support for Facebook local currency payments.

This release is backward-compatible for apps that use the app currency
and Facebook credits decorators.  A future version will remove support
for credits (Facebook will remove them) and app currencies (which can now
use the generic OpenGraph view).


0.2.235
-------

* Packaging fix-ups.


0.2.220
-------

* Fix bug where permissions defined in `facebook.scope` setting were ignored
  by `prompt_authorize`.


0.2.217
-------

* Add view to redirect from GET canvas to the Facebook application page.


0.2.207
-------

* Move predicates from lib to predicates.
* Add `PermissionEventPredicate` for filtering event subscriber with permission.


0.2.2
-----

* Include `pyramid_contextauth` for dealing with context-based authentication.


0.1.194
-------

* Added `CanceledOrder` when any payment update fail during event notification.
* add includeme for any sub module to uniform configuration
* facebook auth policy does not rely anymore on context for authentication.
* add an `CanvasRequested` event triggered when a identified user request
  canvas.


0.1.127
-------

* In credits: Check item title not being an empty string to avoid FB failing with
  no explicit message. "Fail early."
* Fixed bug which raised configuration conflict because `pyramid_facebook` was
  not commiting config via `config.commit`.


0.0
---

*  Initial version
