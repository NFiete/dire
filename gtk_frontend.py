import japanese
import sql_wrapper

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango
from gi.repository import Gdk



class SearchDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Search", transient_for=parent, modal=True)
        self.add_buttons(
            "Exact",
            0,
            "Regex",
            1,
            Gtk.STOCK_CANCEL,
            -1,
        )

        box = self.get_content_area()

        label = Gtk.Label(label="Search")
        box.add(label)

        self.entry = Gtk.Entry()
        box.add(self.entry)

        self.show_all()


class TextViewWindow(Gtk.Window):
    def __init__(self, name, text):
        Gtk.Window.__init__(self, title=name)
        self.title = name

        self.set_default_size(-1, 350)

        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.create_textview(text)
        self.textview.set_editable(False)
        self.size = 23
        tag = self.textbuffer.create_tag("font_size",
                font_desc=Pango.FontDescription.from_string(str(self.size)))
        self.textbuffer.apply_tag(tag, self.textbuffer.get_start_iter(),
                self.textbuffer.get_end_iter())
        #self.textview.set_left_margin(100)
        self.create_buttons()
        self.connect("key-press-event",self.on_key_press_event)
        self.to_begining()

    def to_begining(self):
        self.textbuffer.place_cursor(self.textview.get_buffer().get_iter_at_offset(0))

    def set_text(self, new_text):
        self.textbuffer.set_text(new_text)

    def on_key_press_event(self, widget, event):
        key_name = Gdk.keyval_name(event.keyval)
        if key_name == 'Escape':
            print(not self.textview.get_editable())
            self.textview.set_editable(not self.textview.get_editable())
        elif key_name == 't':
            self.set_text('blah blah blah')
            #dialog = SearchDialog(self)
            #response = dialog.run()
            #dialog.destroy()
        elif key_name == 'l':
            buf = self.textview.get_buffer()
            cur_cur = buf.get_iter_at_mark(buf.get_insert())
            cur_cur.forward_chars(1)
            buf.place_cursor(cur_cur)
        elif key_name == 'h':
            buf = self.textview.get_buffer()
            cur_cur = buf.get_iter_at_mark(buf.get_insert())
            cur_cur.backward_chars(1)
            buf.place_cursor(cur_cur)
        elif key_name == 'j':
            # TODO: There is a better way to do this probably. In the gtk source
            # code they use gtk_widget_class_add_binding_signal (gtktextview.c
            # line 800 is where the use it defined on 4328 of gtkwidget.c) But
            # this aappears to either not be in the python version or I don't
            # know how to do it. If it is the former I might see if I can add it
            # in later of the ladder I will switch.
            cur_cur = self.textbuffer.get_iter_at_mark(self.textbuffer.get_insert())
            loc = self.textview.get_cursor_locations()[0]
            new_cur = self.textview.get_iter_at_location(loc.x, loc.y + loc.height*1.1)[1]
            self.textbuffer.place_cursor(new_cur)
        elif key_name == 'k':
            # TODO: see above. Also this doesn't totally work for paragraphs
            cur_cur = self.textbuffer.get_iter_at_mark(self.textbuffer.get_insert())
            loc = self.textview.get_cursor_locations()[0]
            new_cur = self.textview.get_iter_at_location(loc.x, loc.y - loc.height*.1)[1]
            self.textbuffer.place_cursor(new_cur)
        elif key_name == 'q':
            buf = self.textview.get_buffer()
            cur_cur = buf.get_iter_at_mark(buf.get_insert())
            cur_cur2 = cur_cur.copy()
            cur_cur2.forward_line()
            cur_text = buf.get_text(cur_cur, cur_cur2, False)
            con = sql_wrapper.startConnection('dicts.db')
            words = japanese.start_lookup(cur_text[0:min(len(cur_text), 20)],
                    con)
            new = ''
            for word in words:
                new += word + "\n"
            win = TextViewWindow(self.title + '_0', new)
            win.show_all()
        elif key_name == 'w':
            buf = self.textbuffer
            cur_cur = buf.get_iter_at_mark(buf.get_insert())
            cur_cur2 = cur_cur.copy()
            cur_cur2.forward_line()
            cur_text = buf.get_text(cur_cur, cur_cur2, False)[:-1]
            con = sql_wrapper.startConnection('dicts.db')
            results = sql_wrapper.searchWord(cur_text, con, ['shinmeikai', 'jm'])
            results = list(map(sql_wrapper.toString, results))
            if len(results) == 0:
                return
            new = ''
            for word in results:
                new += word + "---------------------------------\n"
            win = TextViewWindow(self.title + '_0', new)
            win.show_all()

            print(key_name)

        elif key_name == 'g':
            self.textview.get_buffer().place_cursor(self.textview.get_buffer().get_iter_at_offset(0))
        elif key_name == 'p':
            self.size +=1
            tag = self.textbuffer.create_tag("font_size",
                    font_desc=Pango.FontDescription.from_string(str(self.size)))
            self.textbuffer.apply_tag(tag, self.textbuffer.get_start_iter(),
                    self.textbuffer.get_end_iter())
        elif key_name == '-':
            self.size -=1
            tag = self.textbuffer.create_tag("font_size",
                    font_desc=Pango.FontDescription.from_string(str(self.size)))
            self.textbuffer.apply_tag(tag, self.textbuffer.get_start_iter(),
                    self.textbuffer.get_end_iter())



    def create_textview(self, my_text):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.grid.attach(scrolledwindow, 0, 1, 3, 1)

        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text(my_text)
        scrolledwindow.add(self.textview)

        self.tag_bold = self.textbuffer.create_tag("bold", weight=Pango.Weight.BOLD)
        self.tag_italic = self.textbuffer.create_tag("italic", style=Pango.Style.ITALIC)
        self.tag_underline = self.textbuffer.create_tag(
            "underline", underline=Pango.Underline.SINGLE
        )
        self.tag_found = self.textbuffer.create_tag("found", background="yellow")

    def create_buttons(self):
        check_editable = Gtk.CheckButton(label="Editable")
        check_editable.set_active(False)
        check_editable.connect("toggled", self.on_editable_toggled)
        self.grid.attach(check_editable, 0, 2, 1, 1)

        check_cursor = Gtk.CheckButton(label="Cursor Visible")
        check_cursor.set_active(True)
        #check_editable.connect("toggled", self.on_cursor_toggled)
        self.grid.attach_next_to(
            check_cursor, check_editable, Gtk.PositionType.RIGHT, 1, 1
        )

        radio_wrapnone = Gtk.RadioButton.new_with_label_from_widget(None, "No Wrapping")
        self.grid.attach(radio_wrapnone, 0, 3, 1, 1)

        radio_wrapchar = Gtk.RadioButton.new_with_label_from_widget(
            radio_wrapnone, "Character Wrapping"
        )
        self.grid.attach_next_to(
            radio_wrapchar, radio_wrapnone, Gtk.PositionType.RIGHT, 1, 1
        )

        radio_wrapword = Gtk.RadioButton.new_with_label_from_widget(
            radio_wrapnone, "Word Wrapping"
        )
        self.grid.attach_next_to(
            radio_wrapword, radio_wrapchar, Gtk.PositionType.RIGHT, 1, 1
        )

        radio_wrapnone.connect("toggled", self.on_wrap_toggled, Gtk.WrapMode.NONE)
        radio_wrapchar.connect("toggled", self.on_wrap_toggled, Gtk.WrapMode.CHAR)
        radio_wrapword.connect("toggled", self.on_wrap_toggled, Gtk.WrapMode.WORD)

    def on_button_clicked(self, widget, tag):
        bounds = self.textbuffer.get_selection_bounds()
        if len(bounds) != 0:
            start, end = bounds
            self.textbuffer.apply_tag(tag, start, end)

    def on_clear_clicked(self, widget):
        start = self.textbuffer.get_start_iter()
        end = self.textbuffer.get_end_iter()
        self.textbuffer.remove_all_tags(start, end)

    def on_editable_toggled(self, widget):
        self.textview.set_editable(widget.get_active())

    def on_cursor_toggled(self, widget):
        self.textview.set_cursor_visible(widget.get_active())

    def on_wrap_toggled(self, widget, mode):
        self.textview.set_wrap_mode(mode)

    def on_justify_toggled(self, widget, justification):
        self.textview.set_justification(justification)



