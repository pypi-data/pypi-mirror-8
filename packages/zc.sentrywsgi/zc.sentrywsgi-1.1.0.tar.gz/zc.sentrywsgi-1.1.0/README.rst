=================================
WSGI middleware to wire in Sentry
=================================

This is a thin wrapper around the ``raven`` middleware which ensures SSL
validation is performed and logging configuration is also applied.


Release history
===============


1.1.0 (2014-11-26)
------------------

Update to a much newer ``raven``, and get out of the business of
rewiring SSL support.


1.0.1 (2014-11-26)
------------------

Fix ``requests`` dependency to reflect the minimum version that provides
``max_retries`` as a contructor argument for ``requests.adapters.HTTPAdapter``.


1.0.0 (2014-11-24)
------------------

Initial release.
