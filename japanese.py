import sql_wrapper #SQL functions to search database

import re #To check if a word ends with a given string. May remove


'''
The main point of this file is do define the start_lookup method which given a
piece of Japanese text will take the start of it and find all the possible words
the sentance could start with.
It works by:
    TODO: explain
'''

# Return all possible deconjugations do not check if actually a word
def deconjugate_word(word, col, db):
    conjugations = sql_wrapper.get_conjugations(db)
    seen = [word]
    possibilities = [word]
    result = []
    while len(possibilities) > 0:
        cur_word = possibilities.pop()
        for inflection in conjugations:
            if cur_word.endswith(inflection[0]):
                new_word = re.sub(inflection[0] + '$',
                        inflection[1],
                        cur_word)
                if new_word not in seen:
                    possibilities.append(new_word)
                    seen.append(new_word)
                lookup = sql_wrapper.searchWord(new_word, db, col=col)
                result += lookup

    return result


'''
Searches for words at the start of the sentence returns the entries
'''
def starts_with_search(sentance, col, db, deconjugate_json):
    results = []
    i = len(sentance)
    while i > 0 and len(results) < 10:
        substring = sentance[0:i]
        if sql_wrapper.exists_word(substring, db):
            results.append(substring)
            i-=1
            continue
        possible_words = deconjugate_word(substring, col, db, deconjugate_json)
        for word in possible_words:
            if word not in results:
                results.append(word)
        i-=1

    return results


# Converts all katakana to hiragana
def katakana_to_hiragana(word):
    kana_dict= { 'ア': 'あ', 'カ': 'か', 'サ': 'さ', 'タ': 'た', 'ナ': 'な',
            'ハ': 'は', 'マ': 'ま', 'ヤ': 'や', 'ラ': 'ら', 'ワ': 'わ', 'イ':
            'い', 'キ': 'き', 'シ': 'し', 'チ': 'ち', 'ニ': 'に', 'ヒ': 'ひ',
            'ミ': 'み', 'リ': 'り', 'ヰ': 'ゐ', 'ウ': 'う', 'ク': 'く', 'ス':
            'す', 'ツ': 'つ', 'ヌ': 'ぬ', 'フ': 'ふ', 'ム': 'む', 'ユ': 'ゆ',
            'ル': 'る', 'エ': 'え', 'ケ': 'け', 'セ': 'せ', 'テ': 'て', 'ネ':
            'ね', 'ヘ': 'へ', 'メ': 'め', 'レ': 'れ', 'ヱ': 'ゑ', 'オ': 'お',
            'コ': 'こ', 'ソ': 'そ', 'ト': 'と', 'ノ': 'の', 'ホ': 'ほ', 'モ':
            'も', 'ヨ': 'よ', 'ロ': 'ろ', 'ヲ': 'を', 'ン': 'ん', 'ャ': 'ゃ',
            'ュ': 'ゅ', 'ョ': 'ょ', 'ガ': 'が', 'ギ': 'ぎ', 'グ': 'ぐ', 'ゲ':
            'げ', 'ゴ': 'ご', 'ザ': 'ざ', 'ジ': 'じ', 'ズ': 'ず', 'ゼ': 'ぜ',
            'ゾ': 'ぞ', 'ダ': 'だ', 'ヂ': 'ぢ', 'ヅ': 'づ', 'デ': 'で', 'ド':
            'ど', 'バ': 'ば', 'ビ': 'び', 'ブ': 'ぶ', 'ベ': 'べ', 'ボ': 'ぼ',
            'パ': 'ぱ', 'ピ': 'ぴ', 'プ': 'ぷ', 'ペ': 'ぺ', 'ポ': 'ぽ', 'ー':
            'ー', "ッ": "っ"}
    result = ""
    for char in word:
        if char in kana_dict:
            result += kana_dict[char]
        else:
            result += char

    return result

# returns a list with the first number being the number of hiragana the second
# being the number of katakana
def kana_count(sentance):
    katakana = [ 'ア', 'カ', 'サ', 'タ', 'ナ', 'ハ', 'マ', 'ヤ', 'ラ', 'ワ', 'イ', 'キ', 'シ', 'チ', 'ニ', 'ヒ', 'ミ', 'リ', 'ヰ', 'ウ', 'ク', 'ス', 'ツ', 'ヌ', 'フ', 'ム', 'ユ', 'ル', 'エ', 'ケ', 'セ', 'テ', 'ネ', 'ヘ', 'メ', 'レ', 'ヱ', 'オ', 'コ', 'ソ', 'ト', 'ノ', 'ホ', 'モ', 'ヨ', 'ロ', 'ヲ', 'ン', 'ャ', 'ュ', 'ョ' ]
    hiragana = [ 'あ', 'か', 'さ', 'た', 'な', 'は', 'ま', 'や', 'ら', 'わ', 'い', 'き', 'し', 'ち', 'に', 'ひ', 'み', 'り', 'ゐ', 'う', 'く', 'す', 'つ', 'ぬ', 'ふ', 'む', 'ゆ', 'る', 'え', 'け', 'せ', 'て', 'ね', 'へ', 'め', 'れ', 'ゑ', 'お', 'こ', 'そ', 'と', 'の', 'ほ', 'も', 'よ', 'ろ', 'を', 'ん', 'ゃ', 'ゅ', 'ょ' ]
    result = [0, 0]
    for char in sentance:
        if char in hiragana:
            result[0] += 1
        elif char in katakana:
            result[1] += 1

    return result

# Returns true if the function has any kanji in it false otherwise
def has_kanji(sentance):
    katakana = [ 'ア', 'カ', 'サ', 'タ', 'ナ', 'ハ', 'マ', 'ヤ', 'ラ', 'ワ', 'イ', 'キ', 'シ', 'チ', 'ニ', 'ヒ', 'ミ', 'リ', 'ヰ', 'ウ', 'ク', 'ス', 'ツ', 'ヌ', 'フ', 'ム', 'ユ', 'ル', 'エ', 'ケ', 'セ', 'テ', 'ネ', 'ヘ', 'メ', 'レ', 'ヱ', 'オ', 'コ', 'ソ', 'ト', 'ノ', 'ホ', 'モ', 'ヨ', 'ロ', 'ヲ', 'ン', 'ャ', 'ュ', 'ョ' ]
    hiragana = [ 'あ', 'か', 'さ', 'た', 'な', 'は', 'ま', 'や', 'ら', 'わ', 'い', 'き', 'し', 'ち', 'に', 'ひ', 'み', 'り', 'ゐ', 'う', 'く', 'す', 'つ', 'ぬ', 'ふ', 'む', 'ゆ', 'る', 'え', 'け', 'せ', 'て', 'ね', 'へ', 'め', 'れ', 'ゑ', 'お', 'こ', 'そ', 'と', 'の', 'ほ', 'も', 'よ', 'ろ', 'を', 'ん', 'ゃ', 'ゅ', 'ょ' ]
    for char in sentance:
        if char not in katakana and char not in hiragana:
            return True
    return False

# Returns true if the sentance has kanatana it it false otherwise
def has_katakana(sentance):
    katakana = [ 'ア', 'カ', 'サ', 'タ', 'ナ', 'ハ', 'マ', 'ヤ', 'ラ', 'ワ',
            'イ', 'キ', 'シ', 'チ', 'ニ', 'ヒ', 'ミ', 'リ', 'ヰ', 'ウ', 'ク',
            'ス', 'ツ', 'ヌ', 'フ', 'ム', 'ユ', 'ル', 'エ', 'ケ', 'セ', 'テ',
            'ネ', 'ヘ', 'メ', 'レ', 'ヱ', 'オ', 'コ', 'ソ', 'ト', 'ノ', 'ホ',
            'モ', 'ヨ', 'ロ', 'ヲ', 'ン', 'ャ', 'ュ', 'ョ', 'ッ' ]
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
            print(result_possible)
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
        lookup = sql_wrapper.searchWord(substring, db, col=col)
        if len(lookup) > 0:
            results += lookup
            i-=1
            continue
        possible_words = deconjugate_word(substring, col, db)
        for word in possible_words:
            if word not in results:
                results.append(word)
        i-=1
    return results


def start_lookup(sentance, db):
    results = sentance_search(sentance, 'word', db)
    sentance_kana_start = katakana_to_hiragana(start_kana(sentance))
    pronc_results =  sentance_search(sentance_kana_start, 'pronunciation', db)
    for pronc in pronc_results:
        if pronc not in results:
            results.append(pronc)
    if len(results) != 0:
        return results
    possible_pronc = to_hiragana_possible(sentance, db)

    for pronc in possible_pronc:
        results += sentance_search(pronc, 'pronunciation', db)
    return results

