import backend
import japanese
import sql_wrapper
import sys

book = open(sys.argv[1], 'r').read()

reader = backend.text()
reader.text = book

con = sql_wrapper.startConnection('dicts.db')

while True:
    usr = input('> ')
    if usr == 'n':
        reader.forward(1)
    elif usr == 'w':
        reader.forward(5)
    elif usr == 'j':
        reader.forward(20)
    elif usr == 'd':
        print(reader.get_next(20))
    else:
        options = japanese.starts_with_search(reader.get_next(10), 'word', con,
            'deinflect.json')
        print(options)
        usr = input("select an option\n> ")
        result = list(map(sql_wrapper.toString,
            sql_wrapper.searchWord(options[int(usr)], con, ['shinmeikai',
                'daijirin', 'jm', 'daijisen', 'koujien', 'meikyou'])))
        print(result)

