#!/usr/bin/env python

# server program where client sends messages to this
# server using coroutine send/receive

# run this program and then client either on same node or different
# node on local network. Server and client can also be run on two
# different networks but client must call 'scheduler.peer' method
# appropriately.

import sys, logging
# import disasyncoro to use distributed version of AsynCoro
if sys.version_info.major >= 3:
    import disasyncoro3 as asyncoro
else:
    import disasyncoro as asyncoro

def receiver(coro=None):
    coro.set_daemon()
    coro.register('server_coro')
    while True:
        msg = yield coro.receive()
        print('Received %s' % msg)

asyncoro.logger.setLevel(logging.DEBUG)
# call with 'udp_port=0' to start network services
# scheduler = asyncoro.AsynCoro(secret='key')

asyncoro.Coro(receiver)
while True:
    try:
        x = sys.stdin.readline()
    except KeyboardInterrupt:
        break

