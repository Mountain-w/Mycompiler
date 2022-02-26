from simpleLexer import Lexer
from ASTNode import ASTNode
from enums import ASTNodeType, TokenType
from Token import Token


class SimpleParser:
    def parser(self, code):
        lexer = Lexer()
        lexer.token_reader(code)
        tokens = Token(lexer.tokens)
        # print("***词法分析***")
        # for token in lexer.tokens:
        #     print(token.token_type, token.text, sep=' -- ')
        rootNode = self.prog(tokens)
        # print("***语法分析***")
        # self.dumpAST(rootNode, " ")
        return rootNode

    def dumpAST(self, node, indent):
        print(indent, node.node_type, " ", node.text)
        for child in node.children:
            self.dumpAST(child, indent + " --")

    def prog(self, tokens):
        node = ASTNode(ASTNodeType.Programm, "pwc")
        while not tokens.isEmpty():
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
        token = tokens.peek()
        if token and token.token_type == TokenType.Int:
            tokens.popleft()
            token = tokens.peek()
            if token and token.token_type == TokenType.Identifier:
                tokens.popleft()
                node = ASTNode(ASTNodeType.IntDeclaration, token.text)
                token = tokens.peek()
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
                token = tokens.peek()
                if token and token.token_type == TokenType.SemiColon:
                    tokens.popleft()
                else:
                    raise Exception('invalid statement, expecting semicolon')
        return node

    def expressionStatement(self, tokens):
        tokens.getpos()
        node = self.additive(tokens)
        if node:
            token = tokens.peek()
            if token and token.token_type == TokenType.SemiColon:
                tokens.read()
            else:
                node = None
                tokens.setpos()
        return node

    def assignmentStatement(self, tokens):
        node = None
        token = tokens.peek()
        if token and token.token_type == TokenType.Identifier:
            tokens.read()
            node = ASTNode(ASTNodeType.AssignmentStmt, token.text)
            token = tokens.peek()
            if token and token.token_type == TokenType.Assignment:
                tokens.read()
                child = self.additive(tokens)
                if not child:
                    raise Exception("invalid assignment statement,  expecting an expression")
                else:
                    node.addChild(child)
                    token = tokens.peek()
                    if token and token.token_type == TokenType.SemiColon:
                        tokens.read()
                    else:
                        raise Exception("invalid statement, expecting semicolon")
            else:
                tokens.unread()
                node = None
        return node

    def additive(self, tokens):
        child1 = self.multiplicative(tokens)
        node = child1
        if child1:
            while True:
                token = tokens.peek()
                if token and token.token_type in (TokenType.Plus, TokenType.Minus):
                    tokens.read()
                    child2 = self.multiplicative(tokens)
                    if child2:
                        node = ASTNode(ASTNodeType.Additive, token.text)
                        node.addChild(child1)
                        node.addChild(child2)
                        child1 = node
                    else:
                        raise Exception("invalid additive expression, expecting the right part.")
                else:
                    break
        return node

    def multiplicative(self, tokens):
        child1 = self.primary(tokens)
        node = child1

        while True:
            token = tokens.peek()
            if token and token.token_type in (TokenType.Star, TokenType.Slash):
                tokens.read()
                child2 = self.primary(tokens)
                if child2:
                    node = ASTNode(ASTNodeType.Multiplicative, token.text)
                    node.addChild(child1)
                    node.addChild(child2)
                    child1 = node
                else:
                    raise Exception("invalid multiplicative expression, expecting the right part.")
            else:
                break
        return node

    def primary(self, tokens):
        node = None
        token = tokens.peek()
        if token:
            if token.token_type == TokenType.IntLiteral:
                token = tokens.read()
                node = ASTNode(ASTNodeType.IntLiteral, token.text)
            elif token.token_type == TokenType.Identifier:
                token = tokens.read()
                node = ASTNode(ASTNodeType.Identifier, token.text)
            elif token.token_type == TokenType.LeftParen:
                tokens.read()
                node = self.additive(tokens)
                if node:
                    token = tokens.peek()
                    if token and token.token_type == TokenType.RightParen:
                        tokens.read()
                    else:
                        raise Exception("expecting right parenthesis")
                else:
                    raise Exception("expecting an additive expression inside parenthesis")
        return node

# s = SimpleParser()
# s.parser('age=20+1+2;')