from enum import Enum

class TokenTypes(Enum):
    LEFT_PAREN = 'LEFT_PAREN'
    RIGHT_PAREN = 'RIGHT_PAREN'
    LEFT_BRACE = 'LEFT_BRACE'
    RIGHT_BRACE = 'RIGHT_BRACE'
    LEFT_BRACKET = 'LEFT_BRACKET'
    RIGHT_BRACKET = 'RIGHT_BRACKET'
    COMMA = 'COMMA'
    DOT = 'DOT'
    MINUS = 'MINUS'
    PLUS = 'PLUS'
    SEMICOLON = 'SEMICOLON'
    SLASH = 'SLASH'
    STAR = 'STAR'

    BANG = 'BANG'
    BANG_EQUAL = 'BANG_EQUAL'
    EQUAL = 'EQUAL'
    EQUAL_EQUAL = 'EQUAL_EQUAL'
    GREATER = 'GREATER'
    GREATER_EQUAL = 'GREATER_EQUAL'
    LESS = 'LESS'
    LESS_EQUAL = 'LESS_EQUAL'

    IDENTIFIER = 'IDENTIFIER'
    STRING = 'STRING'
    NUMBER = 'NUMBER'

    NIL = 'NIL'
    FALSE = 'FALSE'
    TRUE = 'TRUE'
    AND = 'AND'
    OR = 'OR'
    CLASS = 'CLASS'
    FUN = 'FUN'
    FOR = 'FOR'
    WHILE = 'WHILE'
    IF = 'IF'
    ELIF = 'ELIF'
    ELSE = 'ELSE'
    PRINT = 'PRINT'
    RETURN = 'RETURN'
    SUPER = 'SUPER'
    THIS = 'THIS'
    VAR = 'VAR'

    EOF = 'EOF'


class Token:
    def __init__(self, token_type, lexeme, literal, line):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f"Token<type: {self.token_type}, lexeme: {self.lexeme}, literal: {self.literal}, line: {self.line}>"
