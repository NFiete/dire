import sqlite3
import json
import re
import os


class Entry:
    def __init__(self, word, pronunciaton, meanings, dictonary):
        self.word = word
        self.pronunciation = pronunciaton
        if type(meanings) == list:
            self.meaings = meanings
        else:
            self.meaings = json.loads(meanings)
        self.dictionary = dictonary
    def __str__(self):
        out_str = ['@' + self.dictionary, self.word, self.pronunciation] + self.meaings
        return "\n".join(out_str)
    def __eq__(self, other):
        return self.word == other.word and \
                self.pronunciation == other.pronunciation and \
                self.meaings == other.meaings
    def __ne__(self, other):
        return not self.__eq__(other)



def displayHits(hits):
    for hit in hits:
        print(toString(hit))
        print("-------------------------------------")


def toString(hit):
    out = ""
    dfs = hit[0]
    dct = hit[1]
    if (len(hit[0]) > 0 and len(hit[0][0]) > 0):
        word = hit[0][0][0]
        kana = hit[0][0][1]
        out += dct + "\n"
        out += word + "\n"
        out += kana + "\n"
        for df in dfs:
            defs = json.loads(df[2])
            for treuDf in defs:
                out += treuDf + "\n"
    return out


def hits_to_string(hits):
    strs=[]
    for hit in hits:
        strs.append(toString(hit))
    return '---------------------------\n'.join(strs)


def all_hits_to_string(all_hits):
    strs=[]
    for hit in all_hits:
        strs.append(hits_to_string(hit))
    return '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n'.join(strs)


def clean_query(qry):
    return qry.replace('"', '""')


def displayWords(wordList):
    for word in wordList:
        print(word[0])

def get_conjugations(db):
    return list(db.execute('SELECT * from conjugation'))

def search_glyph(glyph, db):
    glyph = clean_query(glyph)
    qry = f'SELECT pronunciations FROM glyphs WHERE glyph = "{glyph}"'
    results = list(db.execute(qry))
    if len(results) > 0:
        return json.loads(results[0][0])
    return []


'''Searches word from db returning a list of hits. If allDicts is None will
search all dictonaries, otherwise limit to allDicts'''
def searchWord(word, db, col = 'word', allDicts = None):
    word = clean_query(word)
    if allDicts == None:
        qry = f'SELECT * FROM dicts where {col}="{word}"'
    else:
        for i in range(len(allDicts)):
            allDicts[i] = '"' + allDicts[i] + '"'
        in_str = '(' + ','.join(allDicts) + ')'
        #TODO: Also search the word
        qry = f'SELECT * FROM dicts where dict IN "{in_str}"'

    results = list(db.execute(qry).fetchall())
    return list(map(lambda x: Entry(x[1], x[2], x[3], x[4]), results))

def search_pronunciation(pronunciation, db):
    pronunciation = clean_query(pronunciation)
    qry = f'SELECT * FROM dicts WHERE pronunciation="{pronunciation}"'
    results = list(db.execute(qry).fetchall())
    return list(map(lambda x: Entry(x[1], x[2], x[3], x[4]), results))

def pronunciation_exists(pronunciation, db):
    pronunciation = clean_query(pronunciation)
    qry = f'SELECT pronc FROM proncs WHERE pronc="{pronunciation}" LIMIT 1'
    return len(list(db.execute(qry).fetchall())) > 0

def contains_search(term, col, db):
    term = clean_query(term)
    qry=f'SELECT DISTINCT word FROM dicts WHERE {col} LIKE "%{term}%"'
    results = db.execute(qry).fetchall()
    return list(map(lambda x: x[0], results))


def like_search(like_phrase, db):
    like_phrase = clean_query(like_phrase)
    qry = "SELECT word FROM words WHERE word GLOB '" + like_phrase + "'"
    return(list(map(lambda x: x[0], db.execute(qry).fetchall())))

def exists_word(word, db):
    word = clean_query(word)
    qry = f'SELECT word FROM words WHERE word="{word}" LIMIT 1'
    return len(db.execute(qry).fetchall()) > 0


def startConnection():
    home = os.path.expanduser('~')
    con = sqlite3.connect(home + '/.local/share/dire/dire.db')
    con.create_function('regexp', 2, lambda x, y: 1 if re.search(x, y) else 0)
    cur = con.cursor()
    return(cur)

def exists_start(word, col, db):
    word = clean_query(word)
    qry = f'SELECT {col} FROM dicts WHERE {col} LIKE "{word}%" LIMIT 1'
    return len(list(db.execute(qry).fetchall())) > 0

