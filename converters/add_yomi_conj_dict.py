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

def add_file(file, cur):
    deinflect_json = json.loads(open(file, "r").read())
    forms = list(deinflect_json)
    for form in forms:
        for inflection in deinflect_json[form]:
            conjugation = inflection['kanaIn']
            deconjugation = inflection['kanaOut']
            qry = f'SELECT conjugation FROM conjugation  WHERE (conjugation, deconjugation) = ("{conjugation}","{deconjugation}");'
            already_there = cur.execute(qry)
            if len(already_there.fetchall()) == 0:
                qry = f'INSERT INTO conjugation VALUES ("{conjugation}", "{deconjugation}");'
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
add_file(dict_name, cur)
try:
    cur.execute('CREATE INDEX conjugation_idx ON conjugation (conjugation)')
except:
    print('index exists')

con.commit()
con.close()
