import sql_wrapper #SQL functions to search database

import subprocess #To use kakasi to convert to kana
import json #To handle opening the deconjugation list may remove
import re #To check if a word ends with a given string. May remove


'''
The main point of this file is do define the start_lookup method which given a
piece of Japanese text will take the start of it and find all the possible words
the sentance could start with.
It works by:
    TODO: explain
'''

# Return all possible deconjugations do not check if actually a word
def deconjugate_possiblities(word, col, db, deconjugation_list):
    deinflect_json = json.loads(open(deconjugation_list, "r").read())
    forms = list(deinflect_json)
    seen = [word]
    possibilities = [word]
    while len(possibilities) > 0:
        cur_word = possibilities.pop()
        for form in forms:
            for inflection in deinflect_json[form]:
                if cur_word.endswith(inflection['kanaIn']):
                    new_word = re.sub(inflection['kanaIn'] + '$',
                            inflection['kanaOut'],
                            cur_word)
                    if new_word not in seen:
                        possibilities.append(new_word)
                        seen.append(new_word)

    return possibilities


# Go through all possible conjugations and try to de conjugate Only include
# results which are words in col of db
def deconjugate_word(word, col, db, deconjugation_list):
    deinflect_json = json.loads(open(deconjugation_list, "r").read())
    forms = list(deinflect_json)
    seen = [word]
    possibilities = [word]
    results = []
    while len(possibilities) > 0:
        cur_word = possibilities.pop()
        for form in forms:
            for inflection in deinflect_json[form]:
                if cur_word.endswith(inflection['kanaIn']):
                    new_word = re.sub(inflection['kanaIn'] + '$',
                            inflection['kanaOut'],
                            cur_word)
                    if new_word not in seen:
                        possibilities.append(new_word)
                        seen.append(new_word)
                    if sql_wrapper.exists_word(new_word, db):
                        results.append(new_word)

    return results




def starts_with_search(sentance, col, db, deconjugate_json):
    results = []
    i = len(sentance)
    while i > 1 and len(results) < 10:
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
    kana_dict= { 'ア': 'あ',
            'カ': 'か',
            'サ': 'さ',
            'タ': 'た',
            'ナ': 'な',
            'ハ': 'は',
            'マ': 'ま',
            'ヤ': 'や',
            'ラ': 'ら',
            'ワ': 'わ',
            'イ': 'い',
            'キ': 'き',
            'シ': 'し',
            'チ': 'ち',
            'ニ': 'に',
            'ヒ': 'ひ',
            'ミ': 'み',
            'リ': 'り',
            'ヰ': 'ゐ',
            'ウ': 'う',
            'ク': 'く',
            'ス': 'す',
            'ツ': 'つ',
            'ヌ': 'ぬ',
            'フ': 'ふ',
            'ム': 'む',
            'ユ': 'ゆ',
            'ル': 'る',
            'エ': 'え',
            'ケ': 'け',
            'セ': 'せ',
            'テ': 'て',
            'ネ': 'ね',
            'ヘ': 'へ',
            'メ': 'め',
            'レ': 'れ',
            'ヱ': 'ゑ',
            'オ': 'お',
            'コ': 'こ',
            'ソ': 'そ',
            'ト': 'と',
            'ノ': 'の',
            'ホ': 'ほ',
            'モ': 'も',
            'ヨ': 'よ',
            'ロ': 'ろ',
            'ヲ': 'を',
            'ン': 'ん',
            'ャ': 'ゃ',
            'ュ': 'ゅ',
            'ョ': 'ょ'
    }
    result = ""
    for char in word:
        result += kana_dict[char]

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
    katakana = [ 'ア', 'カ', 'サ', 'タ', 'ナ', 'ハ', 'マ', 'ヤ', 'ラ', 'ワ', 'イ', 'キ', 'シ', 'チ', 'ニ', 'ヒ', 'ミ', 'リ', 'ヰ', 'ウ', 'ク', 'ス', 'ツ', 'ヌ', 'フ', 'ム', 'ユ', 'ル', 'エ', 'ケ', 'セ', 'テ', 'ネ', 'ヘ', 'メ', 'レ', 'ヱ', 'オ', 'コ', 'ソ', 'ト', 'ノ', 'ホ', 'モ', 'ヨ', 'ロ', 'ヲ', 'ン', 'ャ', 'ュ', 'ョ' ]
    for char in sentance:
        if char in katakana:
            return True
    return False


