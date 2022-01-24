import sqlite3
import json
import os
import sys

def init_db(name):
    con = sqlite3.connect(name)
    cur = con.cursor()


    cur.execute('''CREATE TABLE dicts (word, pronunciation, definition, dict)''')
    cur.execute('''CREATE TABLE glyphs (glyph, pronunciations)''')
    cur.execute('''CREATE TABLE words (word)''')
    cur.execute('''CREATE TABLE conjugation (conjugation, deconjugation)''')

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
            'ョ': 'ょ',
            'ガ': 'が',
            'ギ': 'ぎ',
            'グ': 'ぐ',
            'ゲ': 'げ',
            'ゴ': 'ご',
            'ザ': 'ざ',
            'ジ': 'じ',
            'ズ': 'ず',
            'ゼ': 'ぜ',
            'ゾ': 'ぞ',
            'ダ': 'だ',
            'ヂ': 'ぢ',
            'ヅ': 'づ',
            'デ': 'で',
            'ド': 'ど',
            'バ': 'ば',
            'ビ': 'び',
            'ブ': 'ぶ',
            'ベ': 'べ',
            'ボ': 'ぼ',
            'パ': 'ぱ',
            'ピ': 'ぴ',
            'プ': 'ぷ',
            'ペ': 'ぺ',
            'ポ': 'ぽ',
            'ー': 'ー'
    }
    result = ""
    for char in word:
        if char in kana_dict:
            result += kana_dict[char]
        else:
            result += char

    return result

def process_onyomi(text):
    text = katakana_to_hiragana(text)
    return text.split(' ')

def process_kunyomi(text):
    result = []
    words = text.split(' ')
    for word in words:
        end_idx = 0
        while end_idx < len(word) and word[end_idx] != '.':
            end_idx+=1
        if word[0:end_idx] not in result:
            result.append(word[0:end_idx])
    return result

def merge(lst1, lst2):
    for itm in lst2:
        if itm not in lst1:
            lst1.append(itm)

def add_one_dict(base_name, dict_name, cur):
    files = os.listdir(base_name + '/' + dict_name)
    for file in files:
        if file=='index.json' or 'tag_bank' in file:
            continue
        dir_name = base_name + '/' + dict_name + '/'
        json_file = open(dir_name + '/' + file)
        data = json.load(json_file)
        for entry in data:
            glyph =  entry[0]
            readings = process_onyomi(entry[1])
            merge(readings, process_kunyomi(entry[2]))
            if "" in readings:
                readings.remove("")
            if len(readings) == 0:
                continue
            exists_dict = cur.execute(f'SELECT glyph FROM glyphs WHERE glyph="{glyph}";')
            if len(exists_dict.fetchall()) > 0:
                qry = f'SELECT pronunciations FROM glyphs WHERE glyph="{glyph}";'
                cur_result = json.loads(list(cur.execute(qry).fetchall())[0][0])
                merge(readings, cur_result)
                readings = json.dumps(readings).replace("'", "''")
                qry = f'UPDATE glyphs SET pronunciations = \'{readings}\' WHERE glyph="{glyph}";'
                cur.execute(qry)
            else:
                readings = json.dumps(readings).replace("'", "''")
                qry = f'INSERT INTO glyphs VALUES (\'{glyph}\', \'{readings}\');'
                cur.execute(qry)


home = os.path.expanduser('~')
if not os.path.exists(home + '/.local/share/dire'):
    print("no directory found creating at {}".format(home + '/.local/share/dire'))
    os.mkdir(home + '/.local/share/dire')

if not os.path.exists(home + '/.local/share/dire/dire.db'):
    print("no db found creating at {}".format(home + '/.local/share/dire/dire.db'))
    init_db(home + '/.local/share/dire/dire.db')


con = sqlite3.connect(home + '/.local/share/dire/dire.db')
cur = con.cursor()

dict_name = sys.argv[1]
files = os.listdir(dict_name)
for file in files:
    add_one_dict(dict_name, file, cur)

cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS glyph_idx ON glyphs (glyph)')
con.commit()
con.close()
