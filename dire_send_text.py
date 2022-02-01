#!/bin/python
import socket, sys, os


def usage():
    print('dire_send_text <NAME> <TEXT>')

if len(sys.argv) < 3:
    usage()

name = sys.argv[1]
text = sys.argv[2]
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
home = os.path.expanduser('~')
s.connect(home + '/.config/dire/sockets/' + name)
s.sendall(bytes(sys.argv[2], 'utf-8'))
