"""
Scanner (Lexer) for the Lox language.
"""

from TokenType import Token, TokenType


class Scanner:
    """Lexical scanner that converts source code into tokens."""

    # Reserved keywords mapping
    keywords = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    def __init__(self, source):
        """
        Initialize the Scanner.

        Args:
            source: The source code string to scan
        """
        self.source = source
        self.tokens = []

        # Track position in source code
        self.start = 0      # Points to first character of lexeme being scanned
        self.current = 0    # Points to current character being considered
        self.line = 1       # Current line number

    def scan_tokens(self):
        """
        Scan the entire source code and return list of tokens.

        Returns:
            List of Token objects
        """
        while not self.is_at_end():
            # We are at the beginning of the next lexeme.
            self.start = self.current
            self.scan_token()

        # Add EOF token at the end
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def is_at_end(self):
        """Check if we've consumed all characters."""
        return self.current >= len(self.source)

    def scan_token(self):
        """Scan a single token."""
        c = self.advance()

        if c == '(':
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ')':
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == '{':
            self.add_token(TokenType.LEFT_BRACE)
        elif c == '}':
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ',':
            self.add_token(TokenType.COMMA)
        elif c == '.':
            self.add_token(TokenType.DOT)
        elif c == '-':
            self.add_token(TokenType.MINUS)
        elif c == '+':
            self.add_token(TokenType.PLUS)
        elif c == ';':
            self.add_token(TokenType.SEMICOLON)
        elif c == '*':
            self.add_token(TokenType.STAR)
        elif c == '!':
            self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
        elif c == '=':
            self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
        elif c == '<':
            self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
        elif c == '>':
            self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
        elif c == '/':
            if self.match('/'):
                # A comment goes until the end of the line.
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif c == ' ' or c == '\r' or c == '\t':
            # Ignore whitespace.
            pass
        elif c == '\n':
            self.line += 1
        elif c == '"':
            self.string()
        else:
            if self.is_digit(c):
                self.number()
            elif self.is_alpha(c):
                self.identifier()
            else:
                # Import Lox here to avoid circular import
                from lox import Lox
                Lox.error(self.line, "Unexpected character.")

    def match(self, expected):
        """
        Check if the current character matches the expected character.
        If it matches, consume it and return True. Otherwise return False.

        Args:
            expected: The character to match

        Returns:
            True if matched and consumed, False otherwise
        """
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self):
        """
        Look at the current character without consuming it (lookahead).

        Returns:
            The current character, or '\0' if at end
        """
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def string(self):
        """Handle string literals."""
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            from lox import Lox
            Lox.error(self.line, "Unterminated string.")
            return

        # The closing ".
        self.advance()

        # Trim the surrounding quotes.
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)

    def is_digit(self, c):
        """
        Check if a character is a digit.

        Args:
            c: Character to check

        Returns:
            True if c is a digit ('0'-'9')
        """
        return c >= '0' and c <= '9'

    def number(self):
        """Handle number literals."""
        while self.is_digit(self.peek()):
            self.advance()

        # Look for a fractional part.
        if self.peek() == '.' and self.is_digit(self.peek_next()):
            # Consume the "."
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()

        value = float(self.source[self.start:self.current])
        self.add_token(TokenType.NUMBER, value)

    def peek_next(self):
        """
        Look ahead two characters without consuming.

        Returns:
            The character after current, or '\0' if at/past end
        """
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def is_alpha(self, c):
        """
        Check if a character is alphabetic or underscore.

        Args:
            c: Character to check

        Returns:
            True if c is a-z, A-Z, or underscore
        """
        return (c >= 'a' and c <= 'z') or \
               (c >= 'A' and c <= 'Z') or \
               c == '_'

    def is_alpha_numeric(self, c):
        """
        Check if a character is alphanumeric or underscore.

        Args:
            c: Character to check

        Returns:
            True if c is a letter, digit, or underscore
        """
        return self.is_alpha(c) or self.is_digit(c)

    def identifier(self):
        """Handle identifiers and keywords."""
        while self.is_alpha_numeric(self.peek()):
            self.advance()

        text = self.source[self.start:self.current]
        token_type = Scanner.keywords.get(text)
        if token_type is None:
            token_type = TokenType.IDENTIFIER
        self.add_token(token_type)

    def advance(self):
        """
        Consume the next character in the source and return it.

        Returns:
            The current character before incrementing
        """
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, token_type, literal=None):
        """
        Add a token to the tokens list.

        Args:
            token_type: The TokenType for this token
            literal: Optional literal value for the token
        """
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))