import japanese
import sql_wrapper
from search_dialog import SearchDialog

import sys, os
import gi
import subprocess
from enum import Enum

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


class Responses(Enum):
    Sentance = 0
    Glob = 1
    Defn = 2


class TextViewWindow(Gtk.Window):
    def __init__(self, name, text, margin=config.default_margin, file_name = None):
        Gtk.Window.__init__(self, title=name)
        self.title = name

        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.set_default_size(config.width, config.height)

        self.create_textview(text)
        self.textview.set_editable(False)
        self.size = config.font_size
        self.font_tag = self.textbuffer.create_tag("font_size",
                font_desc=Pango.FontDescription.from_string(str(self.size)))
        self.textbuffer.apply_tag(self.font_tag, self.textbuffer.get_start_iter(),
                self.textbuffer.get_end_iter())

        self.connect("key-press-event", self.on_key_press_event)
        self.connect("key-release-event", self.on_key_release_event)
        self.to_begining()
        self.con = sql_wrapper.startConnection()

        self.next_mark = False
        self.next_jump = False
        self.control_lock = False
        self.next_perminant_mark = False
        self.next_perminant_jump = False

        self.command = []

        self.cur_search_text = None

        self.text_hist = [text]
        self.text_hist_pos = 0


        self.textview.set_left_margin(margin)
        self.textview.set_right_margin(margin)

        self.file_name = file_name


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
        self.textbuffer.set_text(new_text)
        self.set_font_size()
        self.to_begining()

    def history_back(self):
        if self.text_hist_pos > 0:
            self.text_hist_pos-=1
            self.set_text(self.text_hist[self.text_hist_pos])
            self.to_begining()

    def history_forward(self):
        if self.text_hist_pos < len(self.text_hist) - 1:
            self.text_hist_pos+=1
            self.set_text(self.text_hist[self.text_hist_pos])
            self.to_begining()

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

    def center(self):
        cur = self.textbuffer.get_insert()
        self.textview.scroll_to_mark(cur, 0, True, 0, .5)

    def top(self):
        cur = self.textbuffer.get_insert()
        self.textview.scroll_to_mark(cur, 0, True, 0, 0)

    def add_mark(self, widget, event):
        cur_cur = self.textbuffer.get_iter_at_mark(self.textbuffer.get_insert())
        key_name = Gdk.keyval_name(event.keyval)
        self.textbuffer.create_mark(mark_name=key_name, where = cur_cur)
        self.next_mark = False

    def jump_mark(self, mark):
        my_mark = self.textbuffer.get_mark(mark)
        if my_mark == None:
            self.next_jump = False
            return
        itr = self.textbuffer.get_iter_at_mark(my_mark)
        self.next_jump = False
        self.textbuffer.place_cursor(itr)

    def new_win_lookup_results(self, word, type_lookup):
        if type_lookup == 0:
            words = japanese.start_lookup(word[0:min(len(word),
                config.max_word_len)],
                    self.con)
            if len(words) == 0:
                return ""
            new = "\n".join(map(lambda x: str(x), words))
        elif type_lookup == 1:
            results = sql_wrapper.like_search(word, self.con)
            new = '\n'.join(results)
        elif type_lookup == 2:
            results = sql_wrapper.contains_search(word, 'definition', self.con)
            new = '\n'.join(results)

        return new



    def create_new_win_results(self, text, title):
        win = TextViewWindow(self.title + '-' + title.replace("\n",""), text,
                margin=self.textview.get_left_margin())
        win.show_all()


    def search_term(self, default):
        responses = [("Sentance", Responses.Sentance.value),
                ("Glob", Responses.Glob.value),
                ("Defn", Responses.Defn.value),
                (Gtk.STOCK_CANCEL, -1)]
        search = SearchDialog(self, default, responses, "Query")
        response = search.run()
        if response < 0 or len(search.entry.get_text()) == 0:
            search.hide()
            return
        new = self.new_win_lookup_results(search.entry.get_text(), response)
        self.text_hist.insert(self.text_hist_pos + 1, new)
        self.text_hist_pos += 1
        search.hide()
        self.set_text(new)
        self.to_begining()

    def search_text(self):
        responses = [("Search", Responses.Sentance.value),
                (Gtk.STOCK_CANCEL, -1)]
        search = SearchDialog(self, 0, responses, "Search Text")
        response = search.run()
        if response < 0:
            search.hide()
            return
        self.cur_search_text = search.entry.get_text()
        search.hide()
        self.to_next_forward_search(self.cur_search_text)

    def save_text(self):
        respnses = [
                ("Save", 0),
                (Gtk.STOCK_CANCEL, -1)
                ]
        search = SearchDialog(self, 0, respnses, "Save", self.file_name)
        response = search.run()
        search.hide()
        if response < 0:
            return
        file_name = search.entry.get_text()
        if len(file_name) == 0:
            return

        self.file_name = file_name

        f = open(file_name, "w")
        f.write(self.textbuffer.get_text(self.textbuffer.get_start_iter(),
            self.textbuffer.get_end_iter(), False))



    def to_next_forward_search(self, text_to_find):
        if text_to_find == None:
            return
        cur_cur = self.textbuffer.get_iter_at_mark(self.textbuffer.get_insert())
        cur_cur.forward_chars(1)
        forward = cur_cur.forward_search(text_to_find, 0,\
                self.textbuffer.get_end_iter())
        if forward == None:
            return
        cur_cur = forward[0]
        self.textbuffer.place_cursor(cur_cur)

    def to_previous_backward_search(self, text_to_find):
        if text_to_find == None:
            return
        cur_cur = self.textbuffer.get_iter_at_mark(self.textbuffer.get_insert())
        forward = cur_cur.backward_search(text_to_find, 0,\
                self.textbuffer.get_start_iter())
        if forward == None:
            return
        cur_cur = forward[0]
        self.textbuffer.place_cursor(cur_cur)

    def copy_defn(self):
        forward_cur = self.textbuffer.get_iter_at_mark(self.textbuffer.get_insert())
        while not forward_cur.ends_line():
            forward_cur.forward_char()
        forward = forward_cur.forward_search(config.defn_seperator, 0,\
                self.textbuffer.get_end_iter())

        if forward == None:
            return
        forward = forward[0]

        backward_cur = self.textbuffer.get_iter_at_mark(self.textbuffer.get_insert())
        while not backward_cur.ends_line():
            backward_cur.forward_char()
        backward = backward_cur.backward_search(config.defn_seperator, 0,\
                self.textbuffer.get_start_iter())

        if backward == None:
            backward = self.textbuffer.get_start_iter()
        else:
            backward = backward[0]
        cur_text = self.textbuffer.get_text(backward, forward, False)
        try:
            subprocess.run(config.copy_command.split(),
                    input=cur_text.encode('utf-8'))
        except:
            print('failed to copy')

    def search_clipboard(self):
        try:
            clip = subprocess.run(config.paste_command.split(),
                    capture_output=True, timeout = 1).stdout.decode("utf-8")
        except:
            print('failed to get clipboard')
            return
        new = self.new_win_lookup_results(clip, Responses.Sentance.value)
        self.text_hist.insert(self.text_hist_pos + 1, new)
        self.text_hist_pos += 1
        self.set_text(new)
        self.to_begining()

    def select_text(self, starts, ends, min_left, max_left, min_right, max_right):
        forward_cur = self.textbuffer.get_iter_at_mark(self.textbuffer.get_insert())
        forward_cur.forward_chars(min_right)
        i = 0
        while (max_right == None or i < max_right) and \
            not (forward_cur.get_char() in starts or forward_cur.is_end()):
            forward_cur.forward_char()
            i+=1

        backward_cur = self.textbuffer.get_iter_at_mark(self.textbuffer.get_insert())
        backward_cur.backward_chars(min_left)
        i = 0
        while (max_left == None or i < max_left) and \
            not (backward_cur.get_char() in ends or backward_cur.is_start()):
            backward_cur.backward_char()
            i+=1

        cur_text = self.textbuffer.get_text(backward_cur, forward_cur, False)
        return cur_text

    def make_card(self, text):
        lookup = japanese.start_lookup(text[0:min(len(text), 20)],
                self.con)
        words = list(map(lambda x: x.entries[0].word, lookup))
        defns = list(map(lambda x: list(map(lambda y: str(y), x.entries)), lookup))
        context = self.select_text(config.context_starts, config.context_ends,
                config.min_context_left, config.max_context_left,
                config.min_context_right, config.max_context_right)
        sent = self.select_text(config.card_starts, config.card_ends,
                config.min_sentance_left, config.max_sentance_left,
                config.min_sentance_right, config.max_sentance_right)
        config.make_card(words, defns, sent, context)


    def on_key_release_event(self, widget, event):
        key_name = Gdk.keyval_name(event.keyval)
        if key_name == 'Control_L' or key_name == 'Control_R':
            self.control_lock = False
        if self.control_lock:
            return
        if key_name == config.keybindings['edit_true']:
            self.textview.set_editable(True)


    def inc_margin(self):
        margin = self.textview.get_left_margin()+5
        self.textview.set_left_margin(margin)
        self.textview.set_right_margin(margin)

    def dec_margin(self):
        margin = max(0,self.textview.get_left_margin()-5)
        self.textview.set_left_margin(margin)
        self.textview.set_right_margin(margin)

    def make_perminant_mark(self, mark_name):
        if self.file_name == None:
            # Maybe have a pop-up or something
            print('This is not a file can\'t save a permanent mark. Please save it first')
            return
        offset = self.textbuffer.get_iter_at_mark(self.textbuffer.get_insert()).get_offset()
        home = os.path.expanduser('~')
        if not os.path.exists(home + '/.cache/dire'):
            os.mkdir(home + '/.cache/dire')
        if os.path.exists(home + '/.cache/dire/marks'):
            file = open(home + '/.cache/dire/marks', 'r')
            lines = file.readlines()
            file.close()
        else:
            lines = []
        # Handle various forms of absolute paths
        if self.file_name[0] not in ['/', '~', '.']:
            name = f'{os.getcwd()}/{self.file_name}'
        else:
            name = self.file_name
        # Eliminate (some) edge cases with weird names. If this doesn't work for
        # you it is your own fault
        sep_string =  ':/</>/:'
        name_search = name + sep_string + mark_name + sep_string
        for i in range(len(lines)):
            if lines[i].startswith(name_search):
                lines[i] = f'{name}{sep_string}{mark_name}{sep_string}{offset}\n'
                write_file = open(home + '/.cache/dire/marks', 'w')
                write_file.writelines(lines)
                if lines[-1][-1] != "\n":
                    write_file.write("\n")
                write_file.close()
                return

        write_file = open(home + '/.cache/dire/marks', 'a')
        write_file.write(f'{name}{sep_string}{mark_name}{sep_string}{offset}\n')
        write_file.close()

    def get_perminant_mark(self, mark_name):
        if self.file_name == None:
            # Maybe have a pop-up or something
            print('This is not a file can\'t save a permanent mark. Please save it first')
            return
        home = os.path.expanduser('~')
        if not os.path.exists(home + '/.cache/dire'):
            os.mkdir(home + '/.cache/dire')
            return None
        # Maybe put this in cache?
        if os.path.exists(home + '/.cache/dire/marks'):
            file = open(home + '/.cache/dire/marks', 'r')
        else:
            return None

        sep_string =  ':/</>/:'

        if self.file_name[0] not in ['/', '~', '.']:
            name = f'{os.getcwd()}/{self.file_name}'
        else:
            name = self.file_name

        name_search = name + sep_string + mark_name + sep_string

        line = file.readline()
        while line != '':
            if line.startswith(name_search):
                file.close()
                return int(line.split(sep_string)[-1])
            line = file.readline()

        file.close()
        return None

    def jump_perminant_mark(self, mark_name):
        offset = self.get_perminant_mark(mark_name)
        if offset != None:
            new_iter = self.textbuffer.get_iter_at_offset(offset)
            self.textbuffer.place_cursor(new_iter)


    def multiple_key_command(self, key_name):
        if self.command[0] == 'M':
            self.make_perminant_mark(key_name)
            self.command = []
        elif self.command[0] == 'grave':
            self.command = []
            self.jump_perminant_mark(key_name)



    def on_key_press_event(self, widget, event):
        key_name = Gdk.keyval_name(event.keyval)
        # TODO: Fix the logic of this. Maybe have a string representing the
        # commands and evaluate the string
        if key_name == 'Control_L' or key_name == 'Control_R':
            self.control_lock = True
            return
        if self.control_lock:
            return
        if len(self.command) > 0:
            self.multiple_key_command(key_name)
            return
        if self.next_mark:
            self.add_mark(widget, event)
            return
        if self.next_jump:
            self.jump_mark(key_name)
            return
        elif key_name == config.keybindings['edit_false']:
            self.textview.set_editable(False)
        if self.textview.get_editable():
            return
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
            words = japanese.start_lookup(cur_text[0:min(len(cur_text),
                config.max_word_len)],
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
            new = self.new_win_lookup_results(cur_text, Responses.Sentance.value)
            self.create_new_win_results(new, cur_text)
        elif key_name == config.keybindings['line_search']:
            forward_cur = self.textbuffer.get_iter_at_mark(self.textbuffer.get_insert())
            while not forward_cur.ends_line():
                forward_cur.forward_char()
            backward_cur = self.textbuffer.get_iter_at_mark(self.textbuffer.get_insert())
            while not backward_cur.starts_line():
                backward_cur.backward_char()
            cur_text = self.textbuffer.get_text(backward_cur, forward_cur, False)
            new = self.new_win_lookup_results(cur_text, Responses.Sentance.value)
            self.create_new_win_results(new, cur_text)
        elif key_name == config.keybindings['goto_beginning']:
            self.textbuffer.place_cursor(self.textbuffer.get_iter_at_offset(0))
        elif key_name == config.keybindings['goto_end']:
            self.textbuffer.place_cursor(self.textbuffer.get_end_iter())
        elif key_name == config.keybindings['decrease_font']:
            self.decrease_font_size()
        elif key_name == config.keybindings['increase_font']:
            self.increase_font_size()
        elif key_name == config.keybindings['search_prompt']:
            self.search_term(Responses.Sentance.value)
        elif key_name == config.keybindings['glob_search']:
            self.search_term(Responses.Glob.value)
        elif key_name == config.keybindings['dict_search']:
            self.search_term(Responses.Defn.value)
        elif key_name == config.keybindings['search_text']:
            self.search_text()
        elif key_name == config.keybindings['next_text_search']:
            self.to_next_forward_search(self.cur_search_text)
        elif key_name == config.keybindings['previous_text_search']:
            self.to_previous_backward_search(self.cur_search_text)
        elif key_name == config.keybindings['history_back']:
            self.history_back()
        elif key_name == config.keybindings['history_forward']:
            self.history_forward()
        elif key_name == config.keybindings['next_defn']:
            self.to_next_forward_search(config.defn_seperator)
        elif key_name == config.keybindings['previous_defn']:
            self.to_previous_backward_search(config.defn_seperator)
        elif key_name == config.keybindings['next_result']:
            self.to_next_forward_search(config.result_seperator)
        elif key_name == config.keybindings['previous_result']:
            self.to_previous_backward_search(config.result_seperator)
        elif key_name == config.keybindings['scroll_center']:
            self.center()
        elif key_name == config.keybindings['scroll_top']:
            self.top()
        elif key_name == config.keybindings['copy_defn']:
            self.copy_defn()
        elif key_name == config.keybindings['search_clipboard']:
            self.search_clipboard()
        elif key_name == config.keybindings['make_card']:
            buf = self.textview.get_buffer()
            cur_cur = buf.get_iter_at_mark(buf.get_insert())
            cur_cur2 = cur_cur.copy()
            cur_cur2.forward_line()
            cur_text = buf.get_text(cur_cur, cur_cur2, False)
            self.make_card(cur_text)
        elif key_name == config.keybindings['decrease_margin']:
            self.dec_margin()
        elif key_name == config.keybindings['increase_margin']:
            self.inc_margin()
        elif key_name == config.keybindings['save_current']:
            self.save_text()
        elif key_name == config.keybindings['create_permanent_mark']:
            self.command.append('M')
        elif key_name == config.keybindings['goto_permanent_mark']:
            self.command.append('grave')


    def create_textview(self, my_text):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.grid.attach(scrolledwindow, 0, 1, 3, 1)

        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text(my_text)
        scrolledwindow.add(self.textview)

        self.textview.set_wrap_mode(Gtk.WrapMode.CHAR)




