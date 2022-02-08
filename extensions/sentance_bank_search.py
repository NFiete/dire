import os

def search_sentences(word, orig_text):
    line_bank_dir = os.path.dirname(__file__) + '/line_bank'
    files = os.listdir(line_bank_dir)
    for file in files:
        f = open(line_bank_dir + '/' + file)
        cur_line = f.readline()
        while cur_line != '':
            if word in cur_line:
                return [file, cur_line]
            cur_line = f.readline()
        f.close()
    return None
