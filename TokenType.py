"""
Token types for the Lox language.
"""

from enum import Enum, auto


class TokenType(Enum):
    """Enumeration of all token types in Lox."""

    # Single-character tokens.
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()

    # One or two character tokens.
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    # Literals.
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords.
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()

    EOF = auto()


class Token:
    """Represents a single token in the Lox language."""

    def __init__(self, token_type, lexeme, literal, line):
        """
        Initialize a Token.

        Args:
            token_type: The TokenType enum value
            lexeme: The raw string from the source code
            literal: The literal value (for numbers, strings, etc.)
            line: The line number where the token appears
        """
        self.type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        """Return a string representation of the token."""
        return f"{self.type} {self.lexeme} {self.literal}"

    def __repr__(self):
        """Return a detailed string representation for debugging."""
        return self.__str__()
