dict_order = None

defn_seperator = '@'

result_seperator = '#'

copy_command = 'xclip -selection clipboard'

paste_command = 'xclip -selection clipboard -o'

width = 400
height = 400

font_size = 23

default_margin = 0



keybindings = {
        'search': 'a',
        'line_search': 'e',
        'glob_search': 'r',
        'dict_search': 'd',
        'possible_search': 'q',
        'search_prompt': 's',
        'create_mark': 'm',
        'goto_mark': 'apostrophe',
        'create_permanent_mark': 'M',
        'goto_permanent_mark': 'grave',
        'goto_beginning': 'g',
        'goto_end': 'G',
        'decrease_font': 'minus',
        'increase_font': 'plus',
        'jump_forward': 'w',
        'jump_back': 'b',
        'left': 'h',
        'down': 'j',
        'up': 'k',
        'right': 'l',
        'edit_true': 'i',
        'edit_false': 'Escape',
        'search_text': 'slash',
        'next_text_search': 'n',
        'previous_text_search': 'N',
        'history_back': 'H',
        'history_forward': 'L',
        'next_defn': 'J',
        'previous_defn': 'K',
        'next_result': 'f',
        'previous_result': 'F',
        'scroll_top': 't',
        'scroll_center': 'z',
        'copy_defn': 'y',
        'search_clipboard': 'p',
        'make_card': 'c',
        'decrease_margin': 'bracketleft',
        'increase_margin': 'bracketright',
        'save_current': 'T'
        }

user_defined_searches=[]

user_possible_searches = []

card_starts = ['。', '「', "\n", "、"]
card_ends = ['。', '」', "\n", "、"]

context_starts = ["\n"]
context_ends = ["\n"]

def make_card(words, defns, sentence, context):
    card_file = open('card_file', "a")
    defn_out = ''
    for word,defn in zip(words,defns):
        fix_defn = "<br>".join(defn).replace("\n", "<br>").replace(",", ";")
        defn_out += f'<details><summary>{word}</summary>{fix_defn}</details>'
    sentance = sentence.replace("\n", "<br>").replace(",", ";")
    context = context.replace("\n", "<br>").replace(",", ";")
    card_file.write(f'{sentance},{defn_out},{context}')
    card_file.close()


max_word_len = 20

min_context_left = 100
min_context_right = 0

max_context_left = None
max_context_right = None

min_sentance_left = 5
min_sentance_right = 5

max_sentance_left = 3000
max_sentance_right = 3000

