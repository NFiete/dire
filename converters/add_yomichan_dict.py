import sqlite3
import json
import os
import sys
from japanese import katakana_to_hiragana, has_katakana

tutorial = '''
Thank you for using <FOO_DICT_PROJECT> here are the instructions on
adding yomichan dictionaries..

First gather all of the yomichan dictionaries you want to add into a directory.
Make sure you unzip them and orginize them into folders. So your directory
sturcture should look something like this:
.
├── add_yomichan_dict.py
├── dicts
│   ├── my_dict_1
│   │   ├── term_bank_10.json
│   │   ├── term_bank_11.json
│   │   ├── term_bank_12.json
│   │   ├── ...
│   ├── my_dict_2
│   │   ├── term_bank_10.json
│   │   ├── term_bank_11.json
│   │   ├── term_bank_12.json

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



def init_db(name):
    con = sqlite3.connect(name)
    cur = con.cursor()


    cur.execute('''CREATE TABLE dicts (id integer primary key autoincrement, word, pronunciation, definition, dict)''')
    cur.execute('''CREATE TABLE glyphs (glyph, pronunciations)''')
    cur.execute('''CREATE TABLE words (word)''')
    cur.execute('''CREATE TABLE proncs (pronc, id)''')
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
            word = entry[0].replace("'", "''")
            pronunciation=entry[1].replace("'", "''")
            if has_katakana(pronunciation):
                pronunciation = katakana_to_hiragana(pronunciation)
            definition = json.dumps(entry[5]).replace("'", "''")
            qry = f'INSERT INTO dicts (word, pronunciation, definition, dict) VALUES (\'{word}\', \'{pronunciation}\', \'{definition}\', \'{dict_name}\');'
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

cur.execute('CREATE INDEX IF NOT EXISTS dict_word_index ON dicts (word)')
cur.execute('CREATE INDEX IF NOT EXISTS dict_pron_index ON dicts (pronunciation)')

cur.execute('INSERT INTO words SELECT word FROM dicts WHERE NOT EXISTS (SELECT word FROM words) GROUP BY word;')
cur.execute('CREATE INDEX IF NOT EXISTS word_idx ON words (word)')
con.commit()
con.close()
