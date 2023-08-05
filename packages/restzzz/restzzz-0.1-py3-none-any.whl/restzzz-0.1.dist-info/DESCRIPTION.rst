Documentation
=============

'restzzz' is a tool that is meant to "listen in" on a 0mq connection.

By providing a configuration file, one can specify REST endpoints that listen to a particular 0mq socket.

::

    get:
      zmq:
        connect: tcp://127.0.0.1:8002
        subject: "" # This is the default value, match all messages
      weechat:
        connect: tcp://127.0.0.1:8003
      quilt:
        connect: tcp://some-server:8003
        subject: message
    post:
      zmq:
        connect: tcp://127.0.0.1:8002
        subject: "/sent/via/restzzz"

This creates three endpoints: `zmq`, which can be retrieved from with a GET request and written to with a PUSH request, and `weechat` and `quilt`, which can only be read from.

restzzz makes a few assumptions about the sockets it listens to, mainly that it can connect to them and that they follow the PUB/SUB mentality.


