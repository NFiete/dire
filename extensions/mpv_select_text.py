import japanese
import sql_wrapper

import sys, os
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango
from gi.repository import Gdk


class SelectText(Gtk.Dialog):
    def __init__(self, default, text):
        super().__init__(title="Select 1")

        self.default = default

        box = self.get_content_area()

        new_list = []
        lst_txt = list(text)

        for txt_chr,i in zip(lst_txt, range(len(lst_txt))):
            new_list.append(txt_chr)
            new_list.append(f'[{i}]')



        label = Gtk.Label(label=''.join(new_list))
        box.add(label)

        self.entry = Gtk.Entry()
        box.add(self.entry)

        self.connect("key-press-event", self.enter_return)
        self.show_all()

    def enter_return(self, widget, event):
        key_name = Gdk.keyval_name(event.keyval)
        if key_name == 'Return':
            self.response(self.default)
txt =  'なにか例文'
search = SelectText(0,txt)
response = search.run()
print(txt[int(search.entry.get_text())::])
