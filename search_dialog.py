
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk

class SearchDialog(Gtk.Dialog):
    def __init__(self, parent, default):
        super().__init__(title="Search", transient_for=parent, modal=True)
        self.add_buttons(
            "Sentance",
            0,
            "Glob",
            1,
            "Defn",
            2,
            Gtk.STOCK_CANCEL,
            -1,
        )

        self.default = default

        box = self.get_content_area()

        label = Gtk.Label(label="Search")
        box.add(label)

        self.entry = Gtk.Entry()
        box.add(self.entry)

        self.connect("key-press-event", self.enter_return)
        self.show_all()

    def enter_return(self, widget, event):
        key_name = Gdk.keyval_name(event.keyval)
        if key_name == 'Return':
            self.response(self.default)
