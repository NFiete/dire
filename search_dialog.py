
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk

class SearchDialog(Gtk.Dialog):
    def __init__(self, parent, default, options, title, default_text = ""):
        super().__init__(title=title, transient_for=parent, modal=True)

        for option in options:
            self.add_button(option[0], option[1])

        self.default = default

        box = self.get_content_area()

        label = Gtk.Label(label=title)
        box.add(label)

        self.entry = Gtk.Entry()
        self.entry.set_text(default_text)
        box.add(self.entry)

        self.connect("key-press-event", self.enter_return)
        self.show_all()

    def enter_return(self, widget, event):
        key_name = Gdk.keyval_name(event.keyval)
        if key_name == 'Return':
            self.response(self.default)
