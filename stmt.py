from TokenType import Token
from abc import ABC, abstractmethod

class Visitor(ABC):
    """Visitor interface for AST traversal."""

    @abstractmethod
    def visit_block_stmt(self, stmt):
        """Visit a Block node."""
        pass

    @abstractmethod
    def visit_expression_stmt(self, stmt):
        """Visit a Expression node."""
        pass

    @abstractmethod
    def visit_function_stmt(self, stmt):
        """Visit a Function node."""
        pass

    @abstractmethod
    def visit_if_stmt(self, stmt):
        """Visit a If node."""
        pass

    @abstractmethod
    def visit_print_stmt(self, stmt):
        """Visit a Print node."""
        pass

    @abstractmethod
    def visit_return_stmt(self, stmt):
        """Visit a Return node."""
        pass

    @abstractmethod
    def visit_var_stmt(self, stmt):
        """Visit a Var node."""
        pass

    @abstractmethod
    def visit_while_stmt(self, stmt):
        """Visit a While node."""
        pass


class Stmt:
    """Stmt base class."""

    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor."""
        pass


class Block(Stmt):
    """Block expression."""

    def __init__(self, statements):
        """
        Initialize a Block expression.

        Args:
            statements: List<Stmt>
        """
        self.statements = statements

    def accept(self, visitor):
        """Accept a visitor."""
        return visitor.visit_block_stmt(self)


class Expression(Stmt):
    """Expression expression."""

    def __init__(self, expression):
        """
        Initialize a Expression expression.

        Args:
            expression: Expr
        """
        self.expression = expression

    def accept(self, visitor):
        """Accept a visitor."""
        return visitor.visit_expression_stmt(self)


class Function(Stmt):
    """Function expression."""

    def __init__(self, name, params, body):
        """
        Initialize a Function expression.

        Args:
            name: Token
            params: List<Token>
            body: List<Stmt>
        """
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor):
        """Accept a visitor."""
        return visitor.visit_function_stmt(self)


class If(Stmt):
    """If expression."""

    def __init__(self, condition, thenBranch, elseBranch):
        """
        Initialize a If expression.

        Args:
            condition: Expr
            thenBranch: Stmt
            elseBranch: Stmt
        """
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch

    def accept(self, visitor):
        """Accept a visitor."""
        return visitor.visit_if_stmt(self)


class Print(Stmt):
    """Print expression."""

    def __init__(self, expression):
        """
        Initialize a Print expression.

        Args:
            expression: Expr
        """
        self.expression = expression

    def accept(self, visitor):
        """Accept a visitor."""
        return visitor.visit_print_stmt(self)


class Return(Stmt):
    """Return expression."""

    def __init__(self, keyword, value):
        """
        Initialize a Return expression.

        Args:
            keyword: Token
            value: Expr
        """
        self.keyword = keyword
        self.value = value

    def accept(self, visitor):
        """Accept a visitor."""
        return visitor.visit_return_stmt(self)


class Var(Stmt):
    """Var expression."""

    def __init__(self, name, initializer):
        """
        Initialize a Var expression.

        Args:
            name: Token
            initializer: Expr
        """
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        """Accept a visitor."""
        return visitor.visit_var_stmt(self)


class While(Stmt):
    """While expression."""

    def __init__(self, condition, body):
        """
        Initialize a While expression.

        Args:
            condition: Expr
            body: Stmt
        """
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        """Accept a visitor."""
        return visitor.visit_while_stmt(self)


