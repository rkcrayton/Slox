"""
Parser for the Lox language.
Converts tokens into an Abstract Syntax Tree.
"""

from TokenType import Token, TokenType
from expr import Expr, Binary, Grouping, Literal, Unary


class ParseError(Exception):
    """Exception raised when a parse error occurs."""
    pass


class Parser:
    """Recursive descent parser for Lox expressions."""

    def __init__(self, tokens):
        """
        Initialize the Parser.

        Args:
            tokens: List of tokens from the scanner
        """
        self.tokens = tokens
        self.current = 0

    def parse(self):
        """
        Parse tokens into a list of statements.

        Returns:
            List of Stmt objects, or empty list if error occurred
        """
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())

        return statements

    def declaration(self):
        """
        Parse a declaration.

        declaration → varDecl | statement

        Returns:
            Stmt: The parsed declaration/statement
        """
        try:
            if self.match(TokenType.VAR):
                return self.var_declaration()

            return self.statement()
        except ParseError as error:
            self.synchronize()
            return None

    def var_declaration(self):
        """
        Parse a variable declaration.

        varDecl → "var" IDENTIFIER ( "=" expression )? ";"

        Returns:
            Stmt.Var: The parsed variable declaration
        """
        from stmt import Var

        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")

        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Var(name, initializer)

    def synchronize(self):
        """
        Synchronize after a parse error by discarding tokens until we find a statement boundary.
        """
        self.advance()

        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return

            if self.peek().type in [TokenType.CLASS, TokenType.FUN, TokenType.VAR,
                                   TokenType.FOR, TokenType.IF, TokenType.WHILE,
                                   TokenType.PRINT, TokenType.RETURN]:
                return

            self.advance()

    def expression(self):
        """
        Parse an expression.

        expression → assignment

        Returns:
            Expr: The parsed expression
        """
        return self.assignment()

    def assignment(self):
        """
        Parse an assignment expression.

        assignment → IDENTIFIER "=" assignment | or

        Returns:
            Expr: The parsed expression
        """
        from expr import Assign, Variable

        expr = self.or_expr()

        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()  # Right-associative

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)

            self.error(equals, "Invalid assignment target.")

        return expr

    def or_expr(self):
        """
        Parse an or expression.

        or → and ( "or" and )*

        Returns:
            Expr: The parsed expression
        """
        from expr import Logical

        expr = self.and_expr()

        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.and_expr()
            expr = Logical(expr, operator, right)

        return expr

    def and_expr(self):
        """
        Parse an and expression.

        and → equality ( "and" equality )*

        Returns:
            Expr: The parsed expression
        """
        from expr import Logical

        expr = self.equality()

        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = Logical(expr, operator, right)

        return expr

    def statement(self):
        """
        Parse a statement.

        statement → forStmt | ifStmt | printStmt | whileStmt | blockStmt | exprStmt

        Returns:
            Stmt: The parsed statement
        """
        if self.match(TokenType.FOR):
            return self.for_statement()

        if self.match(TokenType.IF):
            return self.if_statement()

        if self.match(TokenType.PRINT):
            return self.print_statement()

        if self.match(TokenType.WHILE):
            return self.while_statement()

        if self.match(TokenType.LEFT_BRACE):
            return self.block_statement()

        return self.expression_statement()

    def while_statement(self):
        """
        Parse a while statement.

        whileStmt → "while" "(" expression ")" statement

        Returns:
            Stmt.While: The parsed while statement
        """
        from stmt import While

        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body = self.statement()

        return While(condition, body)

    def for_statement(self):
        """
        Parse a for statement (desugared to while).

        forStmt → "for" "(" ( varDecl | exprStmt | ";" )
                           expression? ";"
                           expression? ")" statement

        Returns:
            Stmt: The desugared for loop
        """
        from stmt import Block, Expression, While, Var

        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")

        # Initializer
        initializer = None
        if self.match(TokenType.SEMICOLON):
            initializer = None
        elif self.match(TokenType.VAR):
            initializer = self.var_declaration()
        else:
            initializer = self.expression_statement()

        # Condition
        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        # Increment
        increment = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")

        # Body
        body = self.statement()

        # Desugar: Build the while loop
        # Add increment to body
        if increment is not None:
            body = Block([body, Expression(increment)])

        # Build while loop
        if condition is None:
            from expr import Literal
            condition = Literal(True)
        body = While(condition, body)

        # Add initializer
        if initializer is not None:
            body = Block([initializer, body])

        return body

    def if_statement(self):
        """
        Parse an if statement.

        ifStmt → "if" "(" expression ")" statement ( "else" statement )?

        Returns:
            Stmt.If: The parsed if statement
        """
        from stmt import If

        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch = self.statement()
        else_branch = None
        if self.match(TokenType.ELSE):
            else_branch = self.statement()

        return If(condition, then_branch, else_branch)

    def block_statement(self):
        """
        Parse a block statement.

        block → "{" declaration* "}"

        Returns:
            Stmt.Block: The parsed block statement
        """
        from stmt import Block

        statements = []

        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return Block(statements)

    def print_statement(self):
        """
        Parse a print statement.

        printStmt → "print" expression ";"

        Returns:
            Stmt.Print: The parsed print statement
        """
        from stmt import Print
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def expression_statement(self):
        """
        Parse an expression statement.

        exprStmt → expression ";"

        Returns:
            Stmt.Expression: The parsed expression statement
        """
        from stmt import Expression as ExprStmt
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return ExprStmt(expr)

    def equality(self):
        """
        Parse an equality expression.

        equality → comparison ( ( "!=" | "==" ) comparison )* ;

        Returns:
            Expr: The parsed expression
        """
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self):
        """
        Parse a comparison expression.

        comparison → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;

        Returns:
            Expr: The parsed expression
        """
        expr = self.term()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL,
                         TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self):
        """
        Parse a term expression (addition and subtraction).

        term → factor ( ( "-" | "+" ) factor )* ;

        Returns:
            Expr: The parsed expression
        """
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self):
        """
        Parse a factor expression (multiplication and division).

        factor → unary ( ( "/" | "*" ) unary )* ;

        Returns:
            Expr: The parsed expression
        """
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self):
        """
        Parse a unary expression.

        unary → ( "!" | "-" ) unary
              | primary ;

        Returns:
            Expr: The parsed expression
        """
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self):
        """
        Parse a primary expression.

        primary → NUMBER | STRING | "true" | "false" | "nil"
                | "(" expression ")"
                | IDENTIFIER ;

        Returns:
            Expr: The parsed expression
        """
        if self.match(TokenType.FALSE):
            return Literal(False)

        if self.match(TokenType.TRUE):
            return Literal(True)

        if self.match(TokenType.NIL):
            return Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)

        if self.match(TokenType.IDENTIFIER):
            from expr import Variable
            return Variable(self.previous())

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        # If we get here, we have a token that can't start an expression
        raise self.error(self.peek(), "Expect expression.")

    def consume(self, token_type, message):
        """
        Consume a token of the expected type, or report an error.

        Args:
            token_type: The expected TokenType
            message: Error message if token doesn't match

        Returns:
            Token: The consumed token

        Raises:
            ParseError: If token doesn't match expected type
        """
        if self.check(token_type):
            return self.advance()

        raise self.error(self.peek(), message)

    def error(self, token, message):
        """
        Report a parse error.

        Args:
            token: The token where the error occurred
            message: Error message

        Returns:
            ParseError: The error exception
        """
        from lox import Lox
        Lox.error_token(token, message)
        return ParseError(message)

    def match(self, *types):
        """
        Check if current token matches any of the given types.
        If it matches, consume the token and return True.

        Args:
            *types: Variable number of TokenType values to check

        Returns:
            bool: True if match found and consumed, False otherwise
        """
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True

        return False

    def check(self, token_type):
        """
        Check if current token is of the given type.
        Does not consume the token.

        Args:
            token_type: The TokenType to check

        Returns:
            bool: True if current token matches the type
        """
        if self.is_at_end():
            return False
        return self.peek().type == token_type

    def advance(self):
        """
        Consume the current token and return it.

        Returns:
            Token: The consumed token
        """
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        """
        Check if we're at the end of tokens.

        Returns:
            bool: True if at EOF token
        """
        return self.peek().type == TokenType.EOF

    def peek(self):
        """
        Return current token without consuming it.

        Returns:
            Token: The current token
        """
        return self.tokens[self.current]

    def previous(self):
        """
        Return the previous token.

        Returns:
            Token: The previous token
        """
        return self.tokens[self.current - 1]