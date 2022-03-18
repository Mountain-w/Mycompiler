from enums import ASTNodeType, TokenType
from simpleLexer import Lexer
from collections import deque
from ASTNode import ASTNode


class SimpleCalculator:
    def __init__(self, code):
        self.code = code
        lexer = Lexer()
        lexer.token_reader(code)
        print("***词法分析***")
        for token in lexer.tokens:
            print(token.token_type, token.text, sep=' -- ')
        tokens = deque(lexer.tokens)
        rootnode = self.prog(tokens)
        print("***语法分析***")
        self.dumpAST(rootnode, ' ')

    def dumpAST(self, node, indent):
        print(indent, node.node_type, " ", node.text)
        for child in node.children:
            self.dumpAST(child, indent + " --")

    def prog(self, tokens):
        node = ASTNode(ASTNodeType.Programm, "Calculator")
        child = self.additive(tokens)
        if child:
            node.addChild(child)
        return node

    def intDeclare(self, tokens):
        node = None
        token = None if not tokens else tokens[0]
        if token and token.token_type == TokenType.Int:
            tokens.popleft()
            token = None if not tokens else tokens[0]
            if token and token.token_type == TokenType.Identifier:
                tokens.popleft()
                node = ASTNode(ASTNodeType.Identifier, token.text)
                token = None if not tokens else tokens[0]
                if token and token.token_type == TokenType.Assignment:
                    tokens.popleft()
                    child = self.additive(tokens)
                    if not child:
                        raise Exception('invalid variable initialization, expection an expression')
                    else:
                        node.addChild(child)
            else:
                raise Exception('variable name expected')
            if node:
                token = None if not tokens else tokens[0]
                if token and token.token_type == TokenType.SemiColon:
                    tokens.popleft()
                else:
                    raise Exception('invalid statement, expecting semicolon')
        return node

    def additive(self, tokens):
        """
        语法解析：加法表达式
        :param tokens:
        :return:
        """
        child1 = self.multiplicative(tokens)
        node = child1
        token = None if not tokens else tokens[0]
        if child1 and token:
            if token.token_type in (TokenType.Plus, TokenType.Minus):
                tokens.popleft()
                child2 = self.additive(tokens)
                if child2:
                    node = ASTNode(ASTNodeType.Additive, token.text)
                    node.addChild(child1)
                    node.addChild(child2)
                else:
                    raise Exception("invalid additive expression, expecting the right part.")
        return node

    def multiplicative(self, tokens):
        """
        语法解析：乘法表达式
        :param tokens:
        :return:
        """
        child1 = self.primary(tokens)
        node = child1
        token = None if not tokens else tokens[0]
        if child1 and token:
            if token.token_type in (TokenType.Star, TokenType.Slash):
                tokens.popleft()
                child2 = self.multiplicative(tokens)
                if child2:
                    node = ASTNode(ASTNodeType.Multiplicative, token.text)
                    node.addChild(child1)
                    node.addChild(child2)
                else:
                    raise Exception("invalid multiplicative expression, expecting the right part.")
        return node

    def primary(self, tokens):
        node = None
        token = None if not tokens else tokens[0]
        if token:
            if token.token_type == TokenType.Int:
                node = self.intDeclare(tokens)
            if token.token_type == TokenType.IntLiteral:
                tokens.popleft()
                node = ASTNode(ASTNodeType.IntLiteral, token.text)
            elif token.token_type == TokenType.Identifier:
                tokens.popleft()
                node = ASTNode(ASTNodeType.Identifier, token.text)
            elif token.token_type == TokenType.LeftParen:
                tokens.popleft()
                node = self.additive(tokens)
                if node:
                    token = None if not tokens else tokens[0]
                    if token and token.token_type == TokenType.RightParen:
                        tokens.popleft()
                    else:
                        raise Exception("expecting right parenthesis")
                else:
                    raise Exception('expecting an additive expression inside parenthesis.')
        return node


s = SimpleCalculator('int a = 5;')
