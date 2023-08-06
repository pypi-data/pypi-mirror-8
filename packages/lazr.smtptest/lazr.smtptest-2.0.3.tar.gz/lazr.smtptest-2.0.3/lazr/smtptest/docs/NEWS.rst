======================
NEWS for lazr.smtptest
======================

2.0.3 (2015-01-05)
==================
- Always use old-style namespace package registration in ``lazr/__init__.py``
  since the mere presence of this file subverts PEP 420 style namespace
  packages.  (LP: #1407816)

2.0.2 (2014-08-20)
==================
- Disable `test_suite` in setup.py; nose doesn't work well with
  `python setup.py test` since plugins are disabled.
- Use `python setup.py nosetests` in tox.ini.

2.0.1 (2014-08-19)
==================
- Remove the dependency on `distribute` which has been merged back into
  `setuptools`.  (LP: #1273639)
- Add tox.ini for the preferred way to run the test suite.

2.0 (2013-01-05)
================
- Ported to Python 3.  Now support Python 2.6, 2.7, 3.2, and 3.3.
- Removed the dependency on zc.buildout.
- Use nose for testing.

1.3 (2011-06-07)
================
- Make the test server thread-safe with other code that starts an asyncore
  loop.  Requires Python 2.6 or 2.7.
- Be cleaner about stopping the server: before, it left sockets running
  ans simply cleared out the socket map.  In an associated change, the EXIT
  smtp command sends the reply first, and then shuts down the server, rather
  than the other way around.

1.2 (2009-07-07)
================
- [bug 393621] QueueServer.reset() was added to clear the message queue.  This
  is invoked by sending an SMTP RSET command to the server, or through
  Controller.reset().

1.1 (2009-06-29)
================
- [bug 391650] A non-public API was added to make QueueController more easily
  subclassable.

1.0 (2009-06-22)
================
- Initial release
