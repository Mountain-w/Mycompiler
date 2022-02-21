from enums import DfaState, TokenType


class Token:
    def __init__(self, text=None, token_type=None):
        self.text = text
        self.token_type = token_type


class Lexer:
    def __init__(self):
        self.token_text = []
        self.tokens = []
        self.token = Token()
        self.con = (
            DfaState.GE,
            DfaState.RightParen,
            DfaState.Assignment,
            DfaState.Plus,
            DfaState.Minus,
            DfaState.Star,
            DfaState.Slash,
            DfaState.SemiColon,
            DfaState.LeftParen
        )

    def init_token(self, ch):
        if self.token_text:
            self.token.text = ''.join(self.token_text)
            self.tokens.append(self.token)
            self.token_text = []
            self.token = Token()
        new_state = DfaState.Initial
        if ch.isalpha():
            if ch == 'i':
                new_state = DfaState.Id_int1
            else:
                new_state = DfaState.Id
            self.token.token_type = TokenType.Identifier
            self.token_text.append(ch)
        elif ch.isdigit():
            new_state = DfaState.IntLiteral
            self.token.token_type = TokenType.IntLiteral
            self.token_text.append(ch)
        elif ch == '>':
            new_state = DfaState.GT
            self.token.token_type = TokenType.GT
            self.token_text.append(ch)
        elif ch == '+':
            new_state = DfaState.Plus
            self.token.token_type = TokenType.Plus
            self.token_text.append(ch)
        elif ch == '-':
            new_state = DfaState.Minus
            self.token.token_type = TokenType.Minus
            self.token_text.append(ch)
        elif ch == '*':
            new_state = DfaState.Star
            self.token.token_type = TokenType.Star
            self.token_text.append(ch)
        elif ch == '/':
            new_state = DfaState.Slash
            self.token.token_type = TokenType.Slash
            self.token_text.append(ch)
        elif ch == ';':
            new_state = DfaState.SemiColon
            self.token.token_type = TokenType.SemiColon
            self.token_text.append(ch)
        elif ch == '(':
            new_state = DfaState.LeftParen
            self.token.token_type = TokenType.LeftParen
            self.token_text.append(ch)
        elif ch == ')':
            new_state = DfaState.RightParen
            self.token.token_type = TokenType.RightParen
            self.token_text.append(ch)
        elif ch == '=':
            new_state = DfaState.Assignment
            self.token.token_type = TokenType.Assignment
            self.token_text.append(ch)
        else:
            new_state = DfaState.Initial
        return new_state

    def token_reader(self, code):
        state = DfaState.Initial
        for ch in code:
            if state == DfaState.Initial:
                state = self.init_token(ch)
            elif state == DfaState.Id:
                if ch.isalnum():
                    self.token_text.append(ch)
                else:
                    state = self.init_token(ch)
            elif state == DfaState.GT:
                if ch == '=':
                    self.token.token_type = TokenType.GE
                    state = DfaState.GE
                    self.token_text.append(ch)
                else:
                    state = self.init_token(ch)

            elif state in self.con:
                state = self.init_token(ch)
            elif state == DfaState.IntLiteral:
                if ch.isdigit():
                    self.token_text.append(ch)
                else:
                    state = self.init_token(ch)
            elif state == DfaState.Id_int1:
                if ch == 'n':
                    state = DfaState.Id_int2
                    self.token_text.append(ch)
                elif ch.isalpha:
                    state = DfaState.Id
                    self.token_text.append(ch)
                else:
                    state = self.init_token(ch)
            elif state == DfaState.Id_int2:
                if ch == 't':
                    state = DfaState.Id_int3
                    self.token_text.append(ch)
                elif ch.isalpha:
                    state = DfaState.Id
                    self.token_text.append(ch)
                else:
                    state = self.init_token(ch)
            elif state == DfaState.Id_int3:
                if ch == ' ' or '\t' or '\n':
                    self.token.token_type = TokenType.Int
                    state = self.init_token(ch)
                else:
                    state = DfaState.Id
                    self.token_text.append(ch)
        if self.token_text:
            self.init_token(ch)


# l = Lexer()
# l.token_reader('age = 10')
# for token in l.tokens:
#     print(token.token_type, token.text, sep=' -- ')
