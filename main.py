#!/bin/python
#Maybe change to multipocessing
import threading
import socket
import argparse
import gi
import time
import os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
import gtk_frontend

win = None



home = os.path.expanduser('~')
if not os.path.exists(home + '/.config/dire'):
    os.mkdir(home + '/.config/dire')
    os.mkdir(home + '/.config/dire/sockets')
elif not os.path.exists(home + '/.config/dire/sockets'):
    os.mkdir(home + '/.config/dire/sockets')

parser = argparse.ArgumentParser(description='dictionary integrated reading environment')
parser.add_argument('file', type=str, default=None, nargs='?',
        help='the file to open')
parser.add_argument('-n', '--name', dest='name', default=None,
        help='the name for this instance')

args = parser.parse_args()
file_name = args.file
socket_dir = os.path.expanduser('~') + '/.config/dire/sockets/'
if args.name == None:
    names = ['himari', 'tsumugi', 'rin', 'mei', 'aoi', 'hina', 'mio', 'riko',
            'subaru', 'sora']
    sockets = os.listdir(socket_dir)
    title = str(time.time())
    for name in names:
        if name not in sockets:
            title = name
            break
    name =  socket_dir + title
else:
    title = args.name
    name = os.path.expanduser('~') + '/.config/dire/sockets/' + args.name

if os.path.exists(name):
    print('already exists exiting')
    exit(-1)


if file_name == None:
    my_text = ""
else:
    my_text = open(file_name, 'r').read()
win = gtk_frontend.TextViewWindow(title, my_text)
win.connect("destroy", Gtk.main_quit)


def get_message(conn):
    full_str = ''
    while True:
        data = conn.recv(1024)
        full_str += str(data)
        if not data:
            return full_str

def recvall(sock):
    fragments = []
    while True:
        part = sock.recv(1024)
        if not part:
            # either 0 or end of data
            break
        fragments.append(part)
    return b''.join(fragments)

def listen_for_text(name):
    global win
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.bind(name)
    s.listen(1)
    global win
    while True:
        conn, addr = s.accept()
        my_str = recvall(conn).decode('utf-8')
        if my_str[0] == 's':
            GLib.idle_add(win.set_text, my_str[1::])
        elif my_str[0] == 'a':
            GLib.idle_add(win.append_text, my_str[1::])
        elif my_str[0] == 'p':
            GLib.idle_add(win.push_text, my_str[1::])
        else:
            GLib.idle_add(win.set_text, my_str)



    return 0

x = threading.Thread(target=listen_for_text, args=(name,))
x.daemon = True
x.start()
win.show_all()
Gtk.main()
os.remove(name)
exit(0)
