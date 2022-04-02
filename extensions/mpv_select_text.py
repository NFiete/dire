import gi
import sys

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk


class SelectText(Gtk.Dialog):
    def __init__(self, default, text):
        super().__init__(title="Select 1")

        self.default = default

        box = self.get_content_area()
        box.set_homogeneous(False)

        new_list = []
        lst_txt = list(text)


        for txt_chr,i in zip(lst_txt, range(len(lst_txt))):
            if txt_chr == "\n":
                new_list.append("\n")
                continue
            new_list.append(f'<span size="xx-large">{txt_chr}</span><small>[{i}]</small>')



        label = Gtk.Label()
        label.set_markup(''.join(new_list))
        box.add(label)

        self.entry = Gtk.Entry()
        box.add(self.entry)

        self.connect("key-press-event", self.enter_return)
        self.show_all()

    def enter_return(self, widget, event):
        key_name = Gdk.keyval_name(event.keyval)
        if key_name == 'Return':
            self.response(self.default)

txt =  sys.argv[1]
search = SelectText(0,txt)
response = search.run()
try:
    print(txt[int(search.entry.get_text())::])
except:
    print("None")
