import sql_wrapper
import japanese
import socket

class text:
    def __init__(self):#, text, socket_id):
        self.pos = 0
        '''
        self.text=text
        self.socket_id = 'tjna_dictionary_' + str(socket_id)
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.bind('/tmp/' + self.socket_id)
'''

    def forward(self, by):
        self.pos+=by
        if self.pos > len(self.text):
            self.pos = len(self.text)
        elif self.pos < 0:
            self.pos = 0

    def get_next(self, n):
        if n+self.pos > len(self.text):
            n = len(self.text) - self.pos

        return self.text[self.pos:self.pos+n]

    def next_kanji(self):
        if self.pos == len(self.text):
            return
        self.pos+=1
        while self.pos < len(self.text) and not \
            japanese.has_kanji(self.text[self.pos]):
                self.pos+=1



