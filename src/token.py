from enum import Enum
from typing import TypedDict


class TokenType(Enum):
    DOT = 'DOT'
    COMMA = 'COMMA'
    AMPERSAND = 'AMPERSAND'
    PIPE = 'PIPE'
    SEMICOLON = 'SEMICOLON'
    PAREN_OPEN = 'PAREN_OPEN'
    PAREN_CLOSE = 'PAREN_CLOSE'
    BRACKET_OPEN = 'BRACKET_OPEN'
    BRACKET_CLOSE = 'BRACKET_CLOSE'
    S_BRACKET_OPEN = 'S_BRACKET_OPEN'
    S_BRACKET_CLOSE = 'S_BRACKET_CLOSE'

    PLUS = 'PLUS'
    MINUS = 'MINUS'
    STAR = 'STAR'
    SLASH = 'SLASH'

    EQUAL = 'EQUAL'
    GT = 'GT'
    LT = 'LT'

    PLUS_EQUAL = 'PLUS_EQUAL'
    MINUS_EQUAL = 'MINUS_EQUAL'
    STAR_STAR = 'STAR_STAR'
    SLASH_SLASH = 'SLASH_SLASH'

    BANG_EQUAL = 'BANG_EQUAL'
    EQUAL_EQUAL = 'EQUAL_EQUAL'
    GT_EQUAL = 'GT_EQUAL'
    LT_EQUAL = 'LT_EQUAL'

    # Data Types
    IDENT = 'IDENT'
    STRING = 'STRING'
    INTEGER = 'INTEGER'
    FLOAT = 'FLOAT'

    # Reserved Keywords
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    NIL = 'NIL'
    NOT = 'NOT'
    IS = 'IS'
    AND = 'AND'
    OR = 'OR'

    LET = 'LET'
    CONST = 'CONST'
    IF = 'IF'
    ELIF = 'ELIF'
    ELSE = 'ELSE'
    FOR = 'FOR'
    WHILE = 'WHILE'
    FUN = 'FUN'
    SWITCH = 'SWITCH'
    CASE = 'CASE'
    RETURN = 'RETURN'


class TokenArgs(TypedDict):
    type: TokenType
    lexeme: str | None
    col: tuple[int, int]
    row: tuple[int, int]


class Token:
    def __init__(self, token: TokenArgs) -> None:
        self.type = token.get('type')
        self.lexeme = token.get('lexeme')
        self.col = token.get('col')
        self.row = token.get('row')


    def __repr__(self) -> str:
        return f"<Token(type={self.type}, lexeme={self.lexeme}, col={self.col}, row={self.row})>"
