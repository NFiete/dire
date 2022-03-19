import sql_wrapper #SQL functions to search database
import sys, os # To load config
if os.path.exists(os.path.expanduser('~') + '/.config/dire/config.py'):
    sys.path.append(os.path.expanduser('~') + '/.config/dire/')
elif os.path.exists('/usr/share/dire/config.py'):
    sys.path.append('/usr/share/dire/')
else:
    print("Critical file missing config.py exiting...")
    exit(1)


import re #To check if a word ends with a given string. May remove
import config


'''
The main point of this file is do define the start_lookup method which given a
piece of Japanese text will take the start of it and find all the possible words
the sentance could start with.
It works by:
    TODO: explain
'''


class Entry_Set():
    def __init__(self, entries, orig_len, num_deconjugatins):
        self.entries = entries
        self.orig_len = orig_len
        self.num_deconjugations = num_deconjugatins
        if config.dict_order != None:
            def key(entry):
                return config.dict_order[entry.dictionary]
            entries = sorted(entries, key=key)
        self.entries = entries

    def __lt__(self, other):
        if self.orig_len == other.orig_len:
            return self.num_deconjugations < other.num_deconjugations
        return self.orig_len > other.orig_len
    def __gt__(self, other):
        if self.orig_len == other.orig_len:
            return self.num_deconjugations > other.num_deconjugations
        return self.orig_len < other.orig_len
    def __eq__(self, other):
        return self.entries[0] == other.entries[0]
    def __le__(self, other):
        if self.orig_len == other.orig_len:
            return self.num_deconjugations <= other.num_deconjugations
        return self.orig_len >= other.orig_len
    def __ge__(self, other):
        if self.orig_len == other.orig_len:
            return self.num_deconjugations >= other.num_deconjugations
        return self.orig_len <= other.orig_len
    def __ne__(self, other):
        return self.entries[0] != other.entries[0]
    def __str__(self):
        str_entry = map(str, self.entries)
        return config.result_seperator + '\n'.join(str_entry)


def get_user_results(fun_lst, word, orig_text):
    result = []
    for usr_search in fun_lst:
        if config.dict_order == None or usr_search.__name__ in config.dict_order:
            results = usr_search(word, orig_text)
            if results != None:
                result.append(sql_wrapper.Entry(word, '', results,
                    usr_search.__name__))
    return result

def search_word(word, db, col):
    lookup = sql_wrapper.searchWord(word, db, col=col)
    lookup += get_user_results(config.user_possible_searches, word, word)
    if config.dict_order != None:
        lookup = list(filter(lambda x: x.dictionary in config.dict_order, lookup))
    return lookup


# Return all possible deconjugations do not check if actually a word
def deconjugate_word(word, col, db):
    conjugations = sql_wrapper.get_conjugations(db)
    seen = [word]
    possibilities = [word]
    result = []
    num_conj = 0
    while len(possibilities) > 0:
        cur_word = possibilities.pop()
        for inflection in conjugations:
            if cur_word.endswith(inflection[0]):
                new_word = re.sub(inflection[0] + '$',
                        inflection[1],
                        cur_word)
                num_conj+=1
                if new_word not in seen:
                    possibilities.append(new_word)
                    seen.append(new_word)
                if len(new_word) == 0:
                    continue
                lookup = search_word(new_word, db, col=col)
                if len(lookup) > 0:
                    #This only runs when not an exact match Probably should
                    #refactor
                    usr_results = get_user_results(config.user_defined_searches,
                            new_word, word)
                    result.append(Entry_Set(lookup + usr_results, len(word), num_conj))

    return result



# Converts all katakana to hiragana
def katakana_to_hiragana(word):
    kana_dict= { 'ア': 'あ', 'カ': 'か', 'サ': 'さ', 'タ': 'た', 'ナ': 'な', 'ハ': 'は', 'マ': 'ま', 'ヤ': 'や', 'ラ': 'ら', 'ワ': 'わ', 'イ': 'い', 'キ': 'き', 'シ': 'し', 'チ': 'ち', 'ニ': 'に', 'ヒ': 'ひ', 'ミ': 'み', 'リ': 'り', 'ヰ': 'ゐ', 'ウ': 'う', 'ク': 'く', 'ス': 'す', 'ツ': 'つ', 'ヌ': 'ぬ', 'フ': 'ふ', 'ム': 'む', 'ユ': 'ゆ', 'ル': 'る', 'エ': 'え', 'ケ': 'け', 'セ': 'せ', 'テ': 'て', 'ネ': 'ね', 'ヘ': 'へ', 'メ': 'め', 'レ': 'れ', 'ヱ': 'ゑ', 'オ': 'お', 'コ': 'こ', 'ソ': 'そ', 'ト': 'と', 'ノ': 'の', 'ホ': 'ほ', 'モ': 'も', 'ヨ': 'よ', 'ロ': 'ろ', 'ヲ': 'を', 'ン': 'ん', 'ャ': 'ゃ', 'ュ': 'ゅ', 'ョ': 'ょ', 'ガ': 'が', 'ギ': 'ぎ', 'グ': 'ぐ', 'ゲ': 'げ', 'ゴ': 'ご', 'ザ': 'ざ', 'ジ': 'じ', 'ズ': 'ず', 'ゼ': 'ぜ', 'ゾ': 'ぞ', 'ダ': 'だ', 'ヂ': 'ぢ', 'ヅ': 'づ', 'デ': 'で', 'ド': 'ど', 'バ': 'ば', 'ビ': 'び', 'ブ': 'ぶ', 'ベ': 'べ', 'ボ': 'ぼ', 'パ': 'ぱ', 'ピ': 'ぴ', 'プ': 'ぷ', 'ペ': 'ぺ', 'ポ': 'ぽ', 'ー': 'ー', "ッ": "っ"}
    result = ""
    for char in word:
        if char in kana_dict:
            result += kana_dict[char]
        else:
            result += char

    return result

# Returns true if the function has any kanji in it false otherwise
def has_kanji(sentance):
    katakana = ['ア', 'カ', 'サ', 'タ', 'ナ', 'ハ', 'マ', 'ヤ', 'ラ', 'ワ', 'イ', 'キ', 'シ', 'チ', 'ニ', 'ヒ', 'ミ', 'リ', 'ヰ', 'ウ', 'ク', 'ス', 'ツ', 'ヌ', 'フ', 'ム', 'ユ', 'ル', 'エ', 'ケ', 'セ', 'テ', 'ネ', 'ヘ', 'メ', 'レ', 'ヱ', 'オ', 'コ', 'ソ', 'ト', 'ノ', 'ホ', 'モ', 'ヨ', 'ロ', 'ヲ', 'ン', 'ャ', 'ュ', 'ョ', 'ガ', 'ギ', 'グ', 'ゲ', 'ゴ', 'ザ', 'ジ', 'ズ', 'ゼ', 'ゾ', 'ダ', 'ヂ', 'ヅ', 'デ', 'ド', 'バ', 'ビ', 'ブ', 'ベ', 'ボ', 'パ', 'ピ', 'プ', 'ペ', 'ポ', 'ー', 'ッ']
    hiragana= ['あ', 'か', 'さ', 'た', 'な', 'は', 'ま', 'や', 'ら', 'わ', 'い', 'き', 'し', 'ち', 'に', 'ひ', 'み', 'り', 'ゐ', 'う', 'く', 'す', 'つ', 'ぬ', 'ふ', 'む', 'ゆ', 'る', 'え', 'け', 'せ', 'て', 'ね', 'へ', 'め', 'れ', 'ゑ', 'お', 'こ', 'そ', 'と', 'の', 'ほ', 'も', 'よ', 'ろ', 'を', 'ん', 'ゃ', 'ゅ', 'ょ', 'が', 'ぎ', 'ぐ', 'げ', 'ご', 'ざ', 'じ', 'ず', 'ぜ', 'ぞ', 'だ', 'ぢ', 'づ', 'で', 'ど', 'ば', 'び', 'ぶ', 'べ', 'ぼ', 'ぱ', 'ぴ', 'ぷ', 'ぺ', 'ぽ', 'ー', 'っ']
    for char in sentance:
        if char not in katakana and char not in hiragana:
            return True
    return False

# Returns true if the sentance has kanatana it it false otherwise
def has_katakana(sentance):
    katakana = ['ア', 'カ', 'サ', 'タ', 'ナ', 'ハ', 'マ', 'ヤ', 'ラ', 'ワ', 'イ', 'キ', 'シ', 'チ', 'ニ', 'ヒ', 'ミ', 'リ', 'ヰ', 'ウ', 'ク', 'ス', 'ツ', 'ヌ', 'フ', 'ム', 'ユ', 'ル', 'エ', 'ケ', 'セ', 'テ', 'ネ', 'ヘ', 'メ', 'レ', 'ヱ', 'オ', 'コ', 'ソ', 'ト', 'ノ', 'ホ', 'モ', 'ヨ', 'ロ', 'ヲ', 'ン', 'ャ', 'ュ', 'ョ', 'ガ', 'ギ', 'グ', 'ゲ', 'ゴ', 'ザ', 'ジ', 'ズ', 'ゼ', 'ゾ', 'ダ', 'ヂ', 'ヅ', 'デ', 'ド', 'バ', 'ビ', 'ブ', 'ベ', 'ボ', 'パ', 'ピ', 'プ', 'ペ', 'ポ', 'ー', 'ッ']
    for char in sentance:
        if char in katakana:
            return True
    return False

'''
Work in progress get all possible hiragana for a sentence
'''
def to_hiragana_possible(word, db):
    word = katakana_to_hiragana(word)
    pronc_possible = []
    for glyph in word:
        pronc_possible.append(sql_wrapper.search_glyph(glyph, db))
    possible = ['']
    result_possible = []
    for pronc_glyph,i in zip(pronc_possible, range(len(pronc_possible))):
        if len(pronc_glyph) == 0:
            pronc_glyph = [word[i]]
        og_possibilities = possible
        possible = []
        no_new = True
        for pronc in pronc_glyph:
            for start_possible in og_possibilities:
                contender = start_possible + pronc
                if sql_wrapper.exists_start(contender, 'pronunciation', db):
                    possible.append(contender)
                    no_new = False
        if no_new:
            result_possible = list(map(lambda x: x + word[i::],
                og_possibilities))
            return result_possible
    return result_possible


def start_kana(word):
    i = 0
    while i < len(word) and not has_kanji(word[i]):
        i+=1
    return word[0:i]


def sentance_search(sentance, col, db):
    results = []
    i = len(sentance)
    while i > 0 and len(results) < 10:
        substring = sentance[0:i]
        lookup = search_word(substring, db, col=col)
        if len(lookup) > 0:
            lookup += get_user_results(config.user_defined_searches, substring,
                    substring)
            results.append(Entry_Set(lookup, i, 0))
            #This was a bad idea should put it in deconjugate word
            #continue
        possible_words = deconjugate_word(substring, col, db)
        for word in possible_words:
            if word not in results:
                results.append(word)
        i-=1
    return results



def start_lookup(sentance, db):
    results = sentance_search(sentance, 'word', db)
    sentance_kana_start = katakana_to_hiragana(start_kana(sentance))
    pronc_results = sentance_search(sentance_kana_start, 'pronunciation', db)
    for pronc in pronc_results:
        if pronc not in results:
            results.append(pronc)
    if len(results) != 0:
        return sorted(results)
    possible_pronc = to_hiragana_possible(sentance, db)

    for pronc in possible_pronc:
        results += sentance_search(pronc, 'pronunciation', db)
    return sorted(results)

