import sqlite3
import json
import os
import sys

tutorial = '''
Thank you for using <FOO_DICT_PROJECT> here are the instructions on
adding yomichan dictionaries..

First gather all of the yomichan dictionaries you want to add into a directory.
Make sure you unzip them and orginize them into folders. So your directory
sturcture should look something like this:

add_yomichan_dict.py
dicts/
    my_first_dict/
        term_bank_1.json
        term_bank_2.json
        ...
    my_second_dict/
        term_bank_1.json
        ...

The names of the folders (in this case my_first_dict) are how they will be
stored in the program so choose the names carefully.

Then run "python add_yomichan_dict.py dicts" to add your dictionaries. If you
did not name the top folder dicts you should use what you named it in place of
dict. This operation may take some time. If you did not already initialize the
database this will do it for you. It will not erase any existing data.
'''

if len(sys.argv) < 2:
    print(tutorial)
    exit(1)


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

# Returns true if the sentance has kanatana it it false otherwise
def has_katakana(sentance):
    katakana = [ 'ア', 'カ', 'サ', 'タ', 'ナ', 'ハ', 'マ', 'ヤ', 'ラ', 'ワ', 'イ', 'キ', 'シ', 'チ', 'ニ', 'ヒ', 'ミ', 'リ', 'ヰ', 'ウ', 'ク', 'ス', 'ツ', 'ヌ', 'フ', 'ム', 'ユ', 'ル', 'エ', 'ケ', 'セ', 'テ', 'ネ', 'ヘ', 'メ', 'レ', 'ヱ', 'オ', 'コ', 'ソ', 'ト', 'ノ', 'ホ', 'モ', 'ヨ', 'ロ', 'ヲ', 'ン', 'ャ', 'ュ', 'ョ' ]
    for char in sentance:
        if char in katakana:
            return True
    return False



def init_db(name):
    con = sqlite3.connect(name)
    cur = con.cursor()


    cur.execute('''CREATE TABLE dicts (word, pronunciation, definition, dict)''')
    cur.execute('''CREATE TABLE glyphs (glyph, pronunciations)''')
    cur.execute('''CREATE TABLE words (word)''')
    cur.execute('''CREATE TABLE conjugation (conjugation, deconjugation)''')


def escape(text):
    result = ''
    escaped_chars = ['\'']
    for char in text:
        print(char)
        if char in escaped_chars:
            print('escaping')
            result += '\\'
        result += char
    print('done')

    return result


def add_one_dict(base_name, dict_name, cur):
    files = os.listdir(base_name + '/' + dict_name)
    exists_dict = cur.execute(f'SELECT dict FROM dicts WHERE dict="{dict_name}" LIMIT 1')
    if len(exists_dict.fetchall()) > 0:
        print(f'{dict_name} already exists skipping...')
        return
    for file in files:
        if file=='index.json' or 'tag_bank' in file:
            continue
        print("adding {} to dict".format(file))
        dir_name = base_name + '/' + dict_name + '/'
        json_file = open(dir_name + '/' + file)
        data = json.load(json_file)
        for entry in data:
            # This is just how they are structured there is other information but I
            # don't use it
            word = entry[0].replace("'", "\"")
            pronunciation=entry[1].replace("'", "\"")
            if has_katakana(pronunciation):
                pronunciation = katakana_to_hiragana(pronunciation)
            definition = str(entry[5]).replace("'", "\"")
            qry = f'INSERT INTO dicts VALUES (\'{word}\', \'{pronunciation}\', \'{definition}\', \'{dict_name}\');'
            cur.execute(qry)


home = os.path.expanduser('~')
if not os.path.exists(home + '/.local/share/dire'):
    print("no directory found creating at {}".format(home + '/.local/share/dire'))
    os.mkdir(home + '/.local/share/dire')

if not os.path.exists(home + '/.local/share/dire/dire.db'):
    print("no db found creating at {}".format(home + '/.local/share/dire/dire.db'))
    init_db(home + '/.local/share/dire/dire.db')

dict_name = sys.argv[1]

con = sqlite3.connect(home + '/.local/share/dire/dire.db')
cur = con.cursor()
files = os.listdir(dict_name)
for file in files:
    add_one_dict(dict_name, file, cur)

index_name = dict_name + '_idx'
pron_index_name = f'pron_{dict_name}_idx'
try:
    cur.execute(f'CREATE INDEX {index_name} ON dicts (word)')
#    cur.execute(f'DROP INDEX {index_name};')
except:
    print('creating index')
try:
    cur.execute(f'CREATE INDEX {pron_index_name} ON dicts (pronunciation)')
#    cur.execute(f'DROP INDEX {pron_index_name};')
except:
    print('creating index')

cur.execute('INSERT INTO words SELECT word FROM dicts WHERE NOT EXISTS (SELECT word FROM words) GROUP BY word;')
try:
    cur.execute('CREATE INDEX word_idx ON words (word)')
#    cur.execute('DROP INDEX word_idx;')
except:
    print('updating word list')
con.commit()
con.close()
