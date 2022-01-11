import sqlite3
import json
import re


class Entry:
    def __init__(self, word, kana, meanings):
        self.word = word
        self.kana = kana
        self.meaings = meanings


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


def displayWords(wordList):
    for word in wordList:
        print(word[0])


def searchWordDict(word, dct, db):
    qry = "SELECT word,kana,defn FROM "+dct+" WHERE word='"+word+"'"
    return(db.execute(qry).fetchall())


def searchWord(word, db, allDicts):
    hits = []
    for dct in allDicts:
        qryResult = searchWordDict(word, dct, db)
        if(len(qryResult) > 0):
            hits.append([qryResult, dct])
    return hits


def regexSearch(regex, db):
    regex = '^' + regex + '$'
    qry = "SELECT word FROM words WHERE word REGEXP '" + regex + "'"
    return(list(map(lambda x: x[0], db.execute(qry).fetchall())))

def exists_word(word, db):
    qry = f'SELECT word FROM words WHERE word="{word}" LIMIT 1'
    return len(db.execute(qry).fetchall()) > 0


def startConnection(dbName):
    con = sqlite3.connect(dbName)
    con.create_function('regexp', 2, lambda x, y: 1 if re.search(x, y) else 0)
    cur = con.cursor()
    return(cur)


