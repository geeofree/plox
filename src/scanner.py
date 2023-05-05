from .token import Token, TokenTypes

_RESERVED_KEYWORDS = {
    'nil': TokenTypes.NIL,
    'or': TokenTypes.OR,
    'and': TokenTypes.AND,
    'true': TokenTypes.TRUE,
    'false': TokenTypes.FALSE,
    'if': TokenTypes.IF,
    'elif': TokenTypes.ELIF,
    'else': TokenTypes.ELSE,
    'for': TokenTypes.FOR,
    'while': TokenTypes.WHILE,
    'var': TokenTypes.VAR,
    'fun': TokenTypes.FUN,
    'return': TokenTypes.RETURN,
    'class': TokenTypes.CLASS,
    'super': TokenTypes.SUPER,
    'this': TokenTypes.THIS,
    'print': TokenTypes.PRINT,
}

class Scanner:
    def __init__(self, source):
        self.source = list(source)
        self.tokens = []
        self._start = 0
        self._current = 0
        self._line = 1
        self._reserved_keywords = _RESERVED_KEYWORDS
        self._token_map = {
            '(': lambda: self._add_token(TokenTypes.LEFT_PAREN),
            ')': lambda: self._add_token(TokenTypes.RIGHT_PAREN),

            '[': lambda: self._add_token(TokenTypes.LEFT_BRACKET),
            ']': lambda: self._add_token(TokenTypes.RIGHT_BRACKET),

            '{': lambda: self._add_token(TokenTypes.LEFT_BRACE),
            '}': lambda: self._add_token(TokenTypes.RIGHT_BRACE),

            ',': lambda: self._add_token(TokenTypes.COMMA),
            '.': lambda: self._add_token(TokenTypes.DOT),
            ';': lambda: self._add_token(TokenTypes.SEMICOLON),

            '+': lambda: self._add_token(TokenTypes.PLUS),
            '-': lambda: self._add_token(TokenTypes.MINUS),
            '*': lambda: self._add_token(TokenTypes.STAR),
            '/': lambda: self._add_token(TokenTypes.SLASH),

            '!': lambda: self._add_token(TokenTypes.BANG_EQUAL if self._matches('=') else TokenTypes.BANG),
            '=': lambda: self._add_token(TokenTypes.EQUAL_EQUAL if self._matches('=') else TokenTypes.EQUAL),
            '>': lambda: self._add_token(TokenTypes.GREATER_EQUAL if self._matches('=') else TokenTypes.GREATER),
            '<': lambda: self._add_token(TokenTypes.LESS_EQUAL if self._matches('=') else TokenTypes.LESS),

            '/': lambda: self._read_to_eol() if self._matches('/') else self._add_(TokenTypes.SLASH),
            '"': lambda: self._read_string(),
        }


    def scan_tokens(self):
        while not self._is_eof():
            self._start = self._current
            self._scan_token()

        self.tokens.append(Token(TokenTypes.EOF, None, None, self._line))
        return self.tokens


    def _add_token(self, token_type, literal=None):
        text = ''.join(self.source[self._start:self._current])
        token = Token(token_type, text, literal, self._line)
        self.tokens.append(token)


    def _is_eof(self):
        return self._current >= len(self.source)


    def _scan_token(self):
        c = self._get_char()

        if c == '\n':
            self._line += 1

        add_matched_token = self._token_map.get(c)

        if add_matched_token:
            add_matched_token()
        else:
            self._default_token_matcher(c)


    def _default_token_matcher(self, char):
        if self._is_digit(char):
            self._read_number()
        elif self._is_alpha(char):
            self._read_identifier()


    def _get_char(self):
        c = self.source[self._current]
        self._current += 1
        return c


    def _read_to_eol(self):
        while self._peek() != '\n' and not self._is_eof():
            self._get_char()


    def _peek(self):
        if self._is_eof():
            return '\0'
        return self.source[self._current]


    def _is_digit(self, char):
        return char >= '0' and char <= '9'


    def _is_alpha(self, char):
        return ((char >= 'a' and char <= 'z') or
                (char >= 'A' and char <= 'Z') or
                 char == '_')


    def _is_alpha_numberic(self, char):
        return self._is_alpha(char) or self._is_digit(char)


    def _read_string(self):
        while self._peek() != '"' and not self._is_eof():
            if self._peek() == '\n':
                self._line += 1
            self._get_char()

        if self._is_eof():
            return print("Unterminated string at line {}.".format(self._line))

        self._get_char()
        string = ''.join(self.source[self._start + 1:self._current - 1])
        self._add_token(TokenTypes.STRING, string)


    def _read_number(self):
        while self._is_digit(self._peek()):
            self._get_char()

        if self._peek() == '.' and self._is_digit(self._peek_next()):
            self._get_char()

            while self._is_digit(self._peek()):
                self._get_char()

        number = ''.join(self.source[self._start:self._current])
        self._add_token(TokenTypes.NUMBER, number)


    def _read_identifier(self):
        while self._is_alpha_numberic(self._peek()):
            self._get_char()

        text = ''.join(self.source[self._start:self._current])
        reserved_token_type = self._reserved_keywords.get(text)

        if reserved_token_type:
            self._add_token(reserved_token_type)
        else:
            self._add_token(TokenTypes.IDENTIFIER)


    def _peek_next(self):
        if self._current + 1 >= len(self.source):
            return '\0'
        return self.source[self._current + 1]


    def _matches(self, expected):
        if self._is_eof() or self.source[self._current] != expected:
            return False

        self._current += 1
        return True
