import sql_wrapper
import japanese

class text:
    def __init__(self):
        self.pos = 0
        self.text="NONE"

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


