============
Queue server
============

As shown in the general usage_ document, you can create subclasses of the
Server class to define how you want to handle received messages.  A very
common pattern is to use a Queue to share messages between the controlling
thread and the server thread.  These are nice because, unlike a mailbox based
server, no sorting is required to get the messages out of the server in the
same order they are sent.

.. _usage: usage.html

First, you need a queue.

    >>> try:
    ...     from queue import Empty, Queue
    ... except ImportError:
    ...     # Python 2
    ...     from Queue import Empty, Queue
    >>> queue = Queue()

Then you need a server.

    >>> from lazr.smtptest.server import QueueServer
    >>> server = QueueServer('localhost', 9025, queue)

Finally, you need a controller.

    >>> from lazr.smtptest.controller import Controller
    >>> controller = Controller(server)

Now, start the SMTP server.

    >>> controller.start()

Send the server a bunch of messages.

    >>> import smtplib
    >>> smtpd = smtplib.SMTP()
    >>> code, helo = smtpd.connect('localhost', 9025)
    >>> print(code, str(helo))
    220 ... Python SMTP proxy version ...

    >>> smtpd.sendmail('iperson@example.com', ['jperson@example.com'], """\
    ... From: Irie Person <iperson@example.com>
    ... To: Jeff Person <jperson@example.com>
    ... Subject: A test
    ... Message-ID: <elephant>
    ...
    ... This is a test.
    ... """)
    {}

    >>> smtpd.sendmail('kperson@example.com', ['lperson@example.com'], """\
    ... From: Kari Person <kperson@example.com>
    ... To: Liam Person <lperson@example.com>
    ... Subject: A test
    ... Message-ID: <falcon>
    ...
    ... This is a test.
    ... """)
    {}

    >>> smtpd.sendmail('mperson@example.com', ['nperson@example.com'], """\
    ... From: Mary Person <mperson@example.com>
    ... To: Neal Person <nperson@example.com>
    ... Subject: A test
    ... Message-ID: <goat>
    ...
    ... This is a test.
    ... """)
    {}

All of these messages are available in the queue.

    >>> while True:
    ...     try:
    ...         message = queue.get_nowait()
    ...     except Empty:
    ...         break
    ...     print(message['message-id'])
    <elephant>
    <falcon>
    <goat>

We're done with the controller.

    >>> controller.stop()


Queue controller
================

An even more convenient interface, is to use the QueueController.

    >>> from lazr.smtptest.controller import QueueController
    >>> controller = QueueController('localhost', 9025)
    >>> controller.start()

    >>> smtpd = smtplib.SMTP()
    >>> code, helo = smtpd.connect('localhost', 9025)
    >>> print(code, str(helo))
    220 ... Python SMTP proxy version ...

We now have an SMTP server that we can send some messages to.

    >>> smtpd.sendmail('operson@example.com', ['pperson@example.com'], """\
    ... From: Onua Person <operson@example.com>
    ... To: Paul Person <pperson@example.com>
    ... Subject: A test
    ... Message-ID: <horse>
    ...
    ... This is a test.
    ... """)
    {}

    >>> smtpd.sendmail('qperson@example.com', ['rperson@example.com'], """\
    ... From: Quay Person <qperson@example.com>
    ... To: Raul Person <rperson@example.com>
    ... Subject: A test
    ... Message-ID: <iguana>
    ...
    ... This is a test.
    ... """)
    {}

    >>> smtpd.sendmail('sperson@example.com', ['tperson@example.com'], """\
    ... From: Sean Person <sperson@example.com>
    ... To: Thom Person <tperson@example.com>
    ... Subject: A test
    ... Message-ID: <jackel>
    ...
    ... This is a test.
    ... """)
    {}

And we can dump out all the messages from the controller.

    >>> for message in controller:
    ...     print(message['message-id'])
    <horse>
    <iguana>
    <jackel>

We can send more messages and view them too.

    >>> smtpd.sendmail('uperson@example.com', ['vperson@example.com'], """\
    ... From: Umma Person <uperson@example.com>
    ... To: Vern Person <vperson@example.com>
    ... Subject: A test
    ... Message-ID: <kangaroo>
    ...
    ... This is a test.
    ... """)
    {}

    >>> for message in controller:
    ...     print(message['message-id'])
    <kangaroo>


Resetting
=========

Queue servers support a RSET (reset) method, which empties the queue.

    >>> smtpd.sendmail('wperson@example.com', ['xperson@example.com'], """\
    ... From: Wynn Person <wperson@example.com>
    ... To: Xerx Person <xperson@example.com>
    ... Subject: A test
    ... Message-ID: <llama>
    ...
    ... This is a test.
    ... """)
    {}

    >>> smtpd.sendmail('yperson@example.com', ['zperson@example.com'], """\
    ... From: Yikes Person <yperson@example.com>
    ... To: Zell Person <zperson@example.com>
    ... Subject: A test
    ... Message-ID: <moose>
    ...
    ... This is a test.
    ... """)
    {}

    >>> controller.queue.qsize()
    2
    >>> controller.reset()
    >>> controller.queue.qsize()
    0


Clean up
========

We're done with this controller.

    >>> controller.stop()
