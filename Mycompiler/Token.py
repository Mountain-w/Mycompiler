from copy import deepcopy
from collections import deque
class Token:
    """
    A token stream
    Support read, unread, peek, getpos, setpos
    """
    def __init__(self, tokens):
        self.tokens = deque(tokens)
        self.stack = []
        self.temp = None

    def popleft(self):
        return self.tokens.popleft()

    def peek(self):
        return None if not self.tokens else self.tokens[0]

    def read(self):
        tmp = self.tokens.popleft()
        self.stack.append(tmp)
        return tmp

    def unread(self):
        tmp = self.stack.pop()
        self.tokens.appendleft(tmp)

    def getpos(self):
        self.temp = deepcopy(self.tokens)

    def setpos(self):
        self.tokens = self.temp
        self.temp = None

    def __getitem__(self, item):
        print(item)
        return self.tokens[item]

    def __str__(self):
        return str(self.tokens)

    def isEmpty(self):
        return len(self.tokens) == 0
