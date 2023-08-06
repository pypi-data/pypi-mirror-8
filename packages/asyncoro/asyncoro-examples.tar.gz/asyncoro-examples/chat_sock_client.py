#!/usr/bin/env python

# run at least two instances of this program on either same node or
# multiple nodes on local network, along with 'chat_sock_server.py';
# text typed in a client is sent to the all other clients

import sys, socket, logging, time
import asyncoro

def client_recv(conn, coro=None):
    conn = asyncoro.AsyncSocket(conn)
    while True:
        line = yield conn.recv_msg()
        if not line:
            break
        print(line)

if __name__ == '__main__':
    asyncoro.logger.setLevel(logging.DEBUG)
    # host name or IP address of server is arg1
    if len(sys.argv) > 1:
        host = sys.argv[1]
    else:
        host = ''

    # port used by server is arg2
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    else:
        port = 1234

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    asyncoro.Coro(client_recv, sock)
    # wrap it with asyncoro's synchronous socket so 'send_msg' can be
    # used
    conn = asyncoro.AsyncSocket(sock, blocking=True)

    while True:
        line = sys.stdin.readline().strip()
        if line.lower() == 'exit' or line.lower() == 'quit':
            break
        conn.send_msg(line)
    conn.shutdown(socket.SHUT_WR)
