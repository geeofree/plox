from typing import List
from .grammar import BinaryExpr, LiteralExpr, NotImplementedExpr, UnaryExpr, GroupExpr
from .token import Token, TokenType


class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens


    def parse(self):
        return _Parser(self.tokens).parse()


class _Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.current = 0
        self.total_tokens = len(tokens)


    def parse(self):
        return self.expression()


    def expression(self):
        return self.equality()


    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            operator = self.get_previous_token()
            right = self.comparison()
            expr = BinaryExpr(expr, operator.type, right)
        return expr


    def comparison(self):
        expr = self.term()
        while self.match(TokenType.GT, TokenType.LT, TokenType.GT_EQUAL, TokenType.LT_EQUAL):
            operator = self.get_previous_token()
            right = self.term()
            expr = BinaryExpr(expr, operator.type, right)
        return expr


    def term(self):
        expr = self.factor()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.get_previous_token()
            right = self.factor()
            expr = BinaryExpr(expr, operator.type, right)
        return expr


    def factor(self):
        expr = self.unary()
        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.STAR_STAR, TokenType.SLASH_SLASH):
            operator = self.get_previous_token()
            right = self.unary()
            expr = BinaryExpr(expr, operator.type, right)
        return expr


    def unary(self):
        while self.match(TokenType.MINUS, TokenType.NOT, TokenType.PLUS_PLUS, TokenType.MINUS_MINUS):
            operator = self.get_previous_token()
            right = self.unary()
            return UnaryExpr(operator.type, right)
        return self.primary()


    def primary(self):
        if self.match(TokenType.TRUE):
            return LiteralExpr(True) 
        elif self.match(TokenType.FALSE):
            return LiteralExpr(False) 
        elif self.match(TokenType.NIL):
            return LiteralExpr(None) 
        elif self.match(TokenType.STRING, TokenType.INTEGER, TokenType.FLOAT):
            return LiteralExpr(self.get_previous_token().lexeme) 
        elif self.match(TokenType.PAREN_OPEN):
            expr = self.expression()
            if self.match(TokenType.PAREN_CLOSE):
                return GroupExpr(expr)
        return NotImplementedExpr()


    def match(self, *token_types: TokenType):
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True
        return False


    def check(self, token_type: TokenType):
        return self.is_not_eof() and self.tokens[self.current].type == token_type


    def get_current_token(self):
        return self.tokens[self.current]


    def get_previous_token(self):
        return self.tokens[self.current - 1]


    def advance(self):
        if self.is_not_eof():
            self.current += 1


    def is_not_eof(self):
        return self.current < self.total_tokens
