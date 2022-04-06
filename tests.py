import japanese
import sql_wrapper
import default_config as config

assert 1==1
config.dict_order = None
con = sql_wrapper.startConnection()
def deconj_to_word(results):
    return list(map(lambda x: x.entries[0].word, results))
assert '見る' in deconj_to_word(japanese.deconjugate_word('見た', 'word', con))
assert '見る' in deconj_to_word(japanese.deconjugate_word('みた', 'pronunciation', con))

hiragana =\
"あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわゐゑをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽゃゅょ"
katanaka=\
"アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヰヱヲンガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポャュョ"
assert japanese.katakana_to_hiragana(katanaka) == hiragana
for ch in katanaka:
    assert japanese.has_katakana(ch)

na_results = deconj_to_word(japanese.deconjugate_word('元気な', 'word', con))
def no_dups(lst):
    i = 0
    j = 0
    while i < len(lst):
        j = i+1
        while j < len(lst):
            if lst[i] == lst[j]:
                return False
            j+=1
        i+=1
    return True
assert '元気' in na_results
assert no_dups(na_results)

just_na = na_results = deconj_to_word(japanese.deconjugate_word('な', 'word', con))
for wrd in just_na:
    assert len(wrd) > 0

def entries_sets_to_words(sets):
    seen = []
    for word in sets:
        seen.append(word.entries[0].word)

# Testing gtk

import gtk_frontend

my_text = '''first line.
second line.
'''

win = gtk_frontend.TextViewWindow("testing will die soon", my_text)
assert win.select_text(['.', "\n"], ['.', "\n"], 0, None, 0, None) == "first line"
assert win.select_text([], [], 0, None, 0, None) == my_text
win.set_text("new text")
assert win.select_text([], [], 0, None, 0, None) == "new text"
win.append_text("new2")
assert win.select_text([], [], 0, None, 0, None) == "new text\nnew2"
win.search_term(0)
assert win.select_text([], [], 0, None, 0, None) != "new text\nnew2"
win.history_back()
assert win.select_text([], [], 0, None, 0, None) ==  my_text
assert '新しい' in win.new_win_lookup_results('新しく', 0)
assert '具体的' in win.new_win_lookup_results('具?的', 1)
assert '図書館' in win.new_win_lookup_results('図*', 1)
assert '分散' in win.new_win_lookup_results('"variance"', 2)
