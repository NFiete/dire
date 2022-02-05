import japanese
import sql_wrapper
from search_dialog import SearchDialog

import sys, os
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango
from gi.repository import Gdk


if os.path.exists(os.path.expanduser('~') + '/.config/dire/config.py'):
    sys.path.append(os.path.expanduser('~') + '/.config/dire/')
elif os.path.exists('/usr/share/dire/config.py'):
    sys.path.append('/usr/share/dire/')
else:
    print("Critical file missing config.py exiting...")
    exit(1)

import config

class TextViewWindow(Gtk.Window):
    def __init__(self, name, text):
        Gtk.Window.__init__(self, title=name)
        self.title = name

        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.text = text
        self.create_textview(text)
        self.textview.set_editable(False)
        self.size = 23
        self.font_tag = self.textbuffer.create_tag("font_size",
                font_desc=Pango.FontDescription.from_string(str(self.size)))
        self.textbuffer.apply_tag(self.font_tag, self.textbuffer.get_start_iter(),
                self.textbuffer.get_end_iter())
        self.connect("key-press-event", self.on_key_press_event)
        self.to_begining()
        self.con = sql_wrapper.startConnection()

        self.next_mark = False
        self.next_jump = False

    def set_font_size(self):
        self.textbuffer.apply_tag(self.font_tag, self.textbuffer.get_start_iter(),
                self.textbuffer.get_end_iter())

    def increase_font_size(self):
        self.textbuffer.get_tag_table().remove(self.font_tag)
        self.size+=1
        self.font_tag = self.textbuffer.create_tag("font_size",
                font_desc=Pango.FontDescription.from_string(str(self.size)))
        self.set_font_size()


    def decrease_font_size(self):
        if(self.size > 2):
            self.textbuffer.get_tag_table().remove(self.font_tag)
            self.size-=1
            self.font_tag = self.textbuffer.create_tag("font_size",
                    font_desc=Pango.FontDescription.from_string(str(self.size)))
            self.set_font_size()


    def to_begining(self):
        self.textbuffer.place_cursor(self.textbuffer.get_iter_at_offset(0))

    def set_text(self, new_text):
        self.text = new_text
        self.textbuffer.set_text(new_text)
        self.set_font_size()

    def append_text(self, new_text):
        self.textbuffer.place_cursor(self.textbuffer.get_end_iter())
        self.textbuffer.insert_at_cursor("\n" + new_text)
        self.textbuffer.place_cursor(self.textbuffer.get_end_iter())
        self.set_font_size()
        cur = self.textbuffer.get_insert()
        self.textview.scroll_mark_onscreen(cur)

    def push_text(self, new_text):
        self.to_begining()
        self.textbuffer.insert_at_cursor("\n" + new_text)
        self.to_begining()

    def add_mark(self, widget, event):
        cur_cur = self.textbuffer.get_iter_at_mark(self.textbuffer.get_insert())
        key_name = Gdk.keyval_name(event.keyval)
        self.textbuffer.create_mark(mark_name=key_name, where = cur_cur)
        self.next_mark = False

    def jump_mark(self, mark):
        my_mark = self.textbuffer.get_mark(mark)
        if my_mark == None:
            return
        itr = self.textbuffer.get_iter_at_mark(my_mark)
        self.next_jump = False
        self.textbuffer.place_cursor(itr)

    def new_win_lookup_results(self, word, type_lookup):
        if type_lookup == 0:
            words = japanese.start_lookup(word[0:min(len(word), 20)],
                    self.con)
            if len(words) == 0:
                return
            new = "\n".join(map(lambda x: str(x), words))
        elif type_lookup == 1:
            results = sql_wrapper.like_search(word, self.con)
            new = '\n'.join(results)
        elif type_lookup == 2:
            results = sql_wrapper.contains_search(word, 'definition', self.con)
            new = '\n'.join(results)


        win = TextViewWindow(self.title + '_0', new)
        win.show_all()

    def on_key_press_event(self, widget, event):
        key_name = Gdk.keyval_name(event.keyval)
        if self.next_mark:
            self.add_mark(widget, event)
            return
        if self.next_jump:
            self.jump_mark(key_name)
        elif key_name == 'Escape':
            self.textview.set_editable(not self.textview.get_editable())
        elif key_name == config.keybindings['jump_forward']:
            cur_cur = self.textbuffer.get_iter_at_mark(self.textbuffer.get_insert())
            prev_cur = cur_cur.copy()
            prev_cur.forward_char()

            cur_text = ''
            while not japanese.has_kanji(cur_text):
                if not prev_cur.forward_char():
                    break
                cur_cur.forward_char()
                cur_text = self.textbuffer.get_text(cur_cur, prev_cur, False)
            self.textbuffer.place_cursor(cur_cur)
        elif key_name == config.keybindings['jump_back']:
            cur_cur = self.textbuffer.get_iter_at_mark(self.textbuffer.get_insert())
            prev_cur = cur_cur.copy()
            prev_cur.backward_char()

            cur_text = ''
            while not japanese.has_kanji(cur_text):
                if not prev_cur.backward_char():
                    break
                cur_cur.backward_char()
                cur_text = self.textbuffer.get_text(prev_cur, cur_cur, False)
            self.textbuffer.place_cursor(cur_cur)
        elif key_name == config.keybindings['right']:
            buf = self.textview.get_buffer()
            cur_cur = buf.get_iter_at_mark(buf.get_insert())
            cur_cur.forward_chars(1)
            buf.place_cursor(cur_cur)
        elif key_name == config.keybindings['left']:
            buf = self.textview.get_buffer()
            cur_cur = buf.get_iter_at_mark(buf.get_insert())
            cur_cur.backward_chars(1)
            buf.place_cursor(cur_cur)
        elif key_name == config.keybindings['down']:
            # TODO: There is a better way to do this probably. In the gtk source
            # code they use gtk_widget_class_add_binding_signal (gtktextview.c
            # line 800 is where the use it defined on 4328 of gtkwidget.c) But
            # this aappears to either not be in the python version or I don't
            # know how to do it. If it is the former I might see if I can add it
            # in later of the ladder I will switch.
            cur_cur = self.textbuffer.get_iter_at_mark(self.textbuffer.get_insert())
            loc = self.textview.get_cursor_locations()[0]
            new_cur = self.textview.get_iter_at_location(loc.x, loc.y + loc.height*1.3)[1]
            self.textbuffer.place_cursor(new_cur)
        elif key_name == config.keybindings['up']:
            # TODO: see above. Also this doesn't totally work for paragraphs
            cur_cur = self.textbuffer.get_iter_at_mark(self.textbuffer.get_insert())
            loc = self.textview.get_cursor_locations()[0]
            new_cur = self.textview.get_iter_at_location(loc.x, loc.y - loc.height*.5)[1]
            self.textbuffer.place_cursor(new_cur)
        elif key_name == config.keybindings['possible_search']:
            buf = self.textview.get_buffer()
            cur_cur = buf.get_iter_at_mark(buf.get_insert())
            cur_cur2 = cur_cur.copy()
            cur_cur2.forward_line()
            cur_text = buf.get_text(cur_cur, cur_cur2, False)
            words = japanese.start_lookup(cur_text[0:min(len(cur_text), 20)],
                    self.con)
            new = ''
            seen = []
            for word in words:
                if word.entries[0].word not in seen:
                    new += word.entries[0].word + "\n"
                    seen.append(word.entries[0].word)
            win = TextViewWindow(self.title + '_0', new)
            win.show_all()
        elif key_name == config.keybindings['create_mark']:
            self.next_mark = True
        elif key_name == config.keybindings['goto_mark']:
            self.next_jump = True
        elif key_name == config.keybindings['search']:
            buf = self.textview.get_buffer()
            cur_cur = buf.get_iter_at_mark(buf.get_insert())
            cur_cur2 = cur_cur.copy()
            cur_cur2.forward_line()
            cur_text = buf.get_text(cur_cur, cur_cur2, False)
            self.new_win_lookup_results(cur_text, 0)
        elif key_name == config.keybindings['line_search']:
            buf = self.textbuffer
            cur_cur = buf.get_iter_at_mark(buf.get_insert())
            cur_cur2 = cur_cur.copy()
            cur_cur2.forward_line()
            cur_text = buf.get_text(cur_cur, cur_cur2, False)[:-1]
            self.new_win_lookup_results(cur_text, 0)
        elif key_name == config.keybindings['goto_beginning']:
            self.textbuffer.place_cursor(self.textbuffer.get_iter_at_offset(0))
        elif key_name == config.keybindings['goto_end']:
            self.textbuffer.place_cursor(self.textbuffer.get_end_iter())
        elif key_name == 'p':
            self.size +=1
            tag = self.textbuffer.create_tag("font_size",
                    font_desc=Pango.FontDescription.from_string(str(self.size)))
            self.textbuffer.apply_tag(tag, self.textbuffer.get_start_iter(),
                    self.textbuffer.get_end_iter())
        elif key_name == config.keybindings['decrease_font']:
            self.decrease_font_size()
        elif key_name == config.keybindings['increase_font']:
            self.increase_font_size()
        elif key_name == config.keybindings['search_prompt']:
            search = SearchDialog(self, 0)
            response = search.run()
            if response < 0:
                return
            self.new_win_lookup_results(search.entry.get_text(), response)
            search.hide()
        elif key_name == config.keybindings['dict_search']:
            search = SearchDialog(self, 2)
            response = search.run()
            if response < 0:
                return
            self.new_win_lookup_results(search.entry.get_text(), response)
            search.hide()
        elif key_name == config.keybindings['glob_search']:
            search = SearchDialog(self, 1)
            response = search.run()
            if response < 0:
                return
            self.new_win_lookup_results(search.entry.get_text(), response)
            search.hide()




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
        self.textview.set_wrap_mode(Gtk.WrapMode.CHAR)




