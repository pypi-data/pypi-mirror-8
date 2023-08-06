=============================
Using the SMTP test framework
=============================

The SMTP test framework provides a real SMTP server listening on a port and
speaking the SMTP protocol.  It runs the server in a separate thread so that
the main thread can send it messages, and verify that it received the
messages.

To use, start by defining a subclass of the Server class.

    >>> from lazr.smtptest.server import Server

Override the handle_message() method to do whatever you want to do with the
message.  For example, you might want to pass the message between the threads
via a Queue.

    >>> try:
    ...     from queue import Queue
    ... except ImportError:
    ...     # Python 2
    ...     from Queue import Queue
    >>> queue = Queue()

    >>> class MyServer(Server):
    ...     def handle_message(self, message):
    ...         queue.put(message)

Start a controller, with our new server.

    >>> from lazr.smtptest.controller import Controller
    >>> controller = Controller(MyServer('localhost', 9025))
    >>> controller.start()

Connect to the server...

    >>> from smtplib import SMTP
    >>> smtpd = SMTP()
    >>> code, helo = smtpd.connect('localhost', 9025)
    >>> print(code, str(helo))
    220 ... Python SMTP proxy version ...

...and send it a message.

    >>> smtpd.sendmail('aperson@example.com', ['bperson@example.com'], """\
    ... From: Abby Person <aperson@example.com>
    ... To: Bart Person <bperson@example.com>
    ... Subject: A test
    ... Message-ID: <aardvark>
    ...
    ... Hi Bart, this is a test.
    ... """)
    {}

Now print the message that the server has just received.

    >>> message = queue.get()
    >>> print(message.as_string())
    From: Abby Person <aperson@example.com>
    To: Bart Person <bperson@example.com>
    Subject: A test
    Message-ID: <aardvark>
    X-Peer: 127.0.0.1:...
    X-MailFrom: aperson@example.com
    X-RcptTo: bperson@example.com
    <BLANKLINE>
    Hi Bart, this is a test.

When you're done with the server, stop it via the controller.

    >>> controller.stop()

The server is guaranteed to be stopped.

    >>> # The traceback text is different between Python 2.5 and 2.6.
    >>> import socket
    >>> try:
    ...     smtpd.connect('localhost', 9025)
    ... except socket.error as error:
    ...     errno, message = error.args
    ...     print(message)
    Connection refused


Resetting
=========

The SMTP server can be reset, which defines application specific behavior.
For example, a server which stores messages in an mbox can be sent the RSET
command to clear the mbox.

This server stores messages in Maildir.

    >>> import os
    >>> import mailbox
    >>> import tempfile
    >>> tempdir = tempfile.mkdtemp()
    >>> mailbox_dir = os.path.join(tempdir, 'maildir')

    >>> class MyServer(Server):
    ...     def __init__(self, host, port):
    ...         Server.__init__(self, host, port)
    ...         self._maildir = mailbox.Maildir(mailbox_dir)
    ...
    ...     def handle_message(self, message):
    ...         self._maildir.add(message)
    ...
    ...     def reset(self):
    ...         self._maildir.clear()

    >>> controller = Controller(MyServer('localhost', 9025))
    >>> controller.start()

Now we can send a couple of messages to the server.

    >>> smtpd = SMTP()
    >>> code, helo = smtpd.connect('localhost', 9025)
    >>> print(code, str(helo))
    220 ... Python SMTP proxy version ...

    >>> smtpd.sendmail('cperson@example.com', ['dperson@example.com'], """\
    ... From: Cris Person <cperson@example.com>
    ... To: Dave Person <dperson@example.com>
    ... Subject: A test
    ... Message-ID: <badger>
    ...
    ... Hi Dave, this is a test.
    ... """)
    {}

    >>> smtpd.sendmail('eperson@example.com', ['fperson@example.com'], """\
    ... From: Elly Person <eperson@example.com>
    ... To: Fred Person <fperson@example.com>
    ... Subject: A test
    ... Message-ID: <cougar>
    ...
    ... Hi Fred, this is a test.
    ... """)
    {}

    >>> smtpd.sendmail('gperson@example.com', ['hperson@example.com'], """\
    ... From: Gwen Person <gperson@example.com>
    ... To: Herb Person <hperson@example.com>
    ... Subject: A test
    ... Message-ID: <dingo>
    ...
    ... Hi Herb, this is a test.
    ... """)
    {}

All of these messages are in the mailbox.

    >>> for message_id in sorted(message['message-id']
    ...                          for message in mailbox.Maildir(mailbox_dir)):
    ...     print(message_id)
    <badger>
    <cougar>
    <dingo>

Reading the messages does not affect their appearance in the mailbox.

    >>> for message_id in sorted(message['message-id']
    ...                          for message in mailbox.Maildir(mailbox_dir)):
    ...     print(message_id)
    <badger>
    <cougar>
    <dingo>

But if we reset the server, the messages disappear.

    >>> controller.reset()
    >>> sum(1 for message in mailbox.Maildir(mailbox_dir))
    0


Clean up
========

    >>> # In Python 2.6, this returns a 221, but not in Python 2.5.
    >>> status = smtpd.quit()
    >>> controller.stop()
    >>> import shutil
    >>> shutil.rmtree(tempdir)
