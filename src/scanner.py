from .token import TokenType, Token

class Scanner:
    def __init__(self, source):
        self.source = source


    def scan(self):
        return _Tokenizer(self.source).tokenize()


class _Tokenizer:
    def __init__(self, source):
        self.source = source
        self.source_len = len(source)
        self.head = 0
        self.tail = self.head
        self.col_offset = self.head
        self.line = 1
        self.tokens = []


    def tokenize(self):
        while self.is_not_eof():
            self.get_token()
        return self.tokens


    def get_token(self):
        char = self.get_char()
        match char:
            case " ":
                while self.peek() == char:
                    self.move_head(1)
                    self.move_tail(1)
            case "#":
                while self.peek() != "\n":
                    self.move_head(1)
                    self.move_tail(1)
            case "\n":
                self.move_line(1)
            case ".":
                self.get_char_token(TokenType.DOT)
            case ",":
                self.get_char_token(TokenType.COMMA)
            case "&":
                self.get_char_token(TokenType.AMPERSAND)
            case "|":
                self.get_char_token(TokenType.PIPE)
            case ";":
                self.get_char_token(TokenType.SEMICOLON)
            case "(":
                self.get_char_token(TokenType.PAREN_OPEN)
            case ")":
                self.get_char_token(TokenType.PAREN_CLOSE)
            case "{":
                self.get_char_token(TokenType.BRACKET_OPEN)
            case "}":
                self.get_char_token(TokenType.BRACKET_CLOSE)
            case "[":
                self.get_char_token(TokenType.S_BRACKET_OPEN)
            case "]":
                self.get_char_token(TokenType.S_BRACKET_CLOSE)
            case "+":
                match self.peek():
                    case "=":
                        self.get_compound_char_token(TokenType.PLUS_EQUAL)
                    case "+":
                        self.get_compound_char_token(TokenType.PLUS_PLUS)
                    case _:
                        self.get_char_token(TokenType.PLUS)
            case "-":
                match self.peek():
                    case "=":
                        self.get_compound_char_token(TokenType.MINUS_EQUAL)
                    case "-":
                        self.get_compound_char_token(TokenType.MINUS_MINUS)
                    case _:
                        self.get_char_token(TokenType.MINUS_MINUS)
            case "*":
                match self.peek():
                    case "*":
                        self.get_compound_char_token(TokenType.STAR_STAR)
                    case _:
                        self.get_char_token(TokenType.STAR_STAR)
            case "/":
                match self.peek():
                    case "/":
                        self.get_compound_char_token(TokenType.SLASH_SLASH)
                    case _:
                        self.get_char_token(TokenType.SLASH_SLASH)
            case "=":
                match self.peek():
                    case "=":
                        self.get_compound_char_token(TokenType.EQUAL_EQUAL)
                    case _:
                        self.get_char_token(TokenType.EQUAL)
            case ">":
                match self.peek():
                    case "=":
                        self.get_compound_char_token(TokenType.GT_EQUAL)
                    case _:
                        self.get_char_token(TokenType.GT)
            case "<":
                match self.peek():
                    case "=":
                        self.get_compound_char_token(TokenType.LT_EQUAL)
                    case _:
                        self.get_char_token(TokenType.LT)
            case "'" | '"':
                self.get_string_token(char)
            case _number if self.is_digit(char):
                self.get_number_token()
            case _ident_or_keyword if char == "_" or self.is_alpha(char):
                self.get_ident_or_keyword()
            case _:
                print(f"Unknown symbol: {char}")
        self.move_head(1)
        self.move_tail(1)


    def get_char_token(self, token_type):
        self.add_token(type=token_type, col=self.get_column())


    def get_compound_char_token(self, token_type):
        self.move_tail(1)
        self.add_token(type=token_type, col=self.get_column())
        self.move_head(1)


    def get_string_token(self, char):
        offset = self.col_offset
        self.move_tail(1)
        while self.is_not_eof(index=self.tail) and self.get_char(index=self.tail) != char:
            if self.get_char(index=self.tail) == "\n":
                offset = self.tail
            self.move_tail(1)
        if not self.is_not_eof(index=self.tail):
            # TODO: Fix this so it makes an accurate report
            raise Exception(f"[UNTERMINATED STRING] Line: {self.line} Column: {self.head - offset}")
        else:
            self.move_tail(1)
            lexeme = self.get_lexeme()
            self.move_tail(-1)
            self.add_token(type=TokenType.STRING, lexeme=lexeme, col=self.get_column())
            self.head = self.tail
            if offset != self.col_offset:
                self.col_offset = offset


    def get_number_token(self):
        if self.get_char() == "0" and self.is_digit(self.peek()):
            self.move_tail(1)
            raise Exception(f"Invalid number literal. Line: {self.line} Col: {self.get_column()}")
        token_type = TokenType.INTEGER
        while self.is_digit(self.get_char(index=self.tail)) or self.get_char(index=self.tail) == ".":
            if self.get_char(index=self.tail) == ".":
                if self.is_digit(self.peek(index=self.tail)) and token_type == TokenType.INTEGER:
                    token_type = TokenType.FLOAT
                else:
                    raise Exception(f"Invalid number literal. Line: {self.line} Col: {self.get_column()}")
            self.move_tail(1)
        lexeme = self.get_lexeme()
        self.move_tail(-1)
        self.add_token(type=token_type, lexeme=lexeme, col=self.get_column())
        self.head = self.tail


    def get_ident_or_keyword(self):
        if self.get_char() == "_" and self.is_digit(self.peek()):
            self.move_tail(1)
            raise Exception(f"Invalid identifier. Line: {self.line} Col: {self.get_column()}")
        while self.is_alphanum(self.get_char(index=self.tail)):
            self.move_tail(1)
        lexeme = self.get_lexeme()
        self.move_tail(-1)
        token_type = None
        match lexeme:
            case "true":
                token_type = TokenType.TRUE
            case "false":
                token_type = TokenType.FALSE
            case "not":
                token_type = TokenType.NOT
            case "is":
                token_type = TokenType.IS
            case "and":
                token_type = TokenType.AND
            case "or":
                token_type = TokenType.OR
            case "let":
                token_type = TokenType.LET
            case "const":
                token_type = TokenType.CONST
            case "if":
                token_type = TokenType.IF
            case "elif":
                token_type = TokenType.ELIF
            case "else":
                token_type = TokenType.ELSE
            case "for":
                token_type = TokenType.FOR
            case "while":
                token_type = TokenType.WHILE
            case "fun":
                token_type = TokenType.FUN
            case "switch":
                token_type = TokenType.SWITCH
            case "case":
                token_type = TokenType.CASE
            case "return":
                token_type = TokenType.RETURN
            case _:
                token_type = TokenType.IDENT
        self.add_token(type=token_type, lexeme=lexeme, col=self.get_column())
        self.head = self.tail


    def add_token(self, **token):
        self.tokens.append(Token(**token, row=self.line))


    def peek(self, **kwargs):
        return self.source[kwargs.get('index', self.head) + 1]


    def get_char(self, **kwargs):
        return self.source[kwargs.get('index', self.head)]


    def get_column(self):
        return (self.head - self.col_offset, self.tail - self.col_offset)


    def get_lexeme(self):
        return self.source[self.head:self.tail]


    def is_not_eof(self, **kwargs):
        return kwargs.get('index', self.head) < self.source_len


    def is_digit(self, char):
        return char >= '0' and char <= '9'


    def is_alpha(self, char):
        return (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z')


    def is_alphanum(self, char):
        return self.is_digit(char) or self.is_alpha(char)


    def move_head(self, amount):
        self.head = self.head + amount


    def move_tail(self, amount):
        self.tail = self.tail + amount


    def move_line(self, amount):
        self.line = self.line + amount
        self.col_offset = self.head
