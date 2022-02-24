from simpleLexer import Lexer
from ASTNode import ASTNode
from collections import deque
from enums import ASTNodeType, TokenType


class SimpleParser:
    def __init__(self, code):
        lexer = Lexer()
        tokens = deque(lexer.tokens)
        self.rootNode = self.prog(tokens)

    def prog(self, tokens):
        node = ASTNode(ASTNodeType.Programm, "pwc")
        while tokens:
            child = self.intDeclare(tokens)
            if not child:
                child = self.expressionStatement(tokens)
            if not child:
                child = self.assignmentStatement(tokens)
            if child:
                node.addChild(child)
            else:
                raise Exception("Unknown Statement")
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

    def expressionStatement(self, tokens):
        return 0

    def assignmentStatement(self, tokens):
        return 0
