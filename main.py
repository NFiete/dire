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



parser = argparse.ArgumentParser(description='tjna japanese reader')
parser.add_argument('file', type=str,
        help='the file to open')
parser.add_argument('-n', '--name', dest='name', default=None,
        help='the name for this instance')

args = parser.parse_args()
file_name = args.file
if args.name == None:
    title = str(time.time())
    name = os.path.expanduser('~') + '/.config/tjna/' + title
else:
    title = args.name
    name = os.path.expanduser('~') + '/.config/tjna/' + args.name

if os.path.exists(name):
    print('already exists esiting')
    exit(-1)


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
    data = b''
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
        GLib.idle_add(win.set_text, my_str)
    return 0

x = threading.Thread(target=listen_for_text, args=(name,))
x.daemon = True
x.start()
win.show_all()
Gtk.main()

