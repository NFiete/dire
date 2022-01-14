import japanese
import sql_wrapper

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango
from gi.repository import Gdk

class TextViewWindow(Gtk.Window):
    def __init__(self, text):
        Gtk.Window.__init__(self, title="tjna")

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

    def on_key_press_event(self, widget, event):
        key_name = Gdk.keyval_name(event.keyval)
        if key_name == 'l':
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
            buf = self.textview.get_buffer()
            cur_cur = buf.get_iter_at_mark(buf.get_insert())
            self.textview.forward_display_line(cur_cur)
            buf.place_cursor(cur_cur)
        elif key_name == 'k':
            buf = self.textview.get_buffer()
            cur_cur = buf.get_iter_at_mark(buf.get_insert())
            offset = cur_cur.get_visible_line_offset()
            cur_cur.backward_lines(1)
            cur_cur.set_visible_line_offset(offset)
            buf.place_cursor(cur_cur)
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
            win = TextViewWindow(new)
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
            win = TextViewWindow(new)
            win.show_all()

        elif key_name == 'a':
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
        self.textbuffer.set_text( my_text)
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


my_text = open('wagahai_wa_neko_de_aru', 'r').read()
win = TextViewWindow(my_text)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
