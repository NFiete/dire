import sqlite3
import json
import os
import sys
from japanese import katakana_to_hiragana

def init_db(name):
    con = sqlite3.connect(name)
    cur = con.cursor()


    cur.execute('''CREATE TABLE dicts (word, pronunciation, definition, dict)''')
    cur.execute('''CREATE TABLE glyphs (glyph, pronunciations)''')
    cur.execute('''CREATE TABLE words (word)''')
    cur.execute('''CREATE TABLE conjugation (conjugation, deconjugation)''')

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
