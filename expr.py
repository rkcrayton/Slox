from TokenType import Token
from abc import ABC, abstractmethod

class Visitor(ABC):
    """Visitor interface for AST traversal."""

    @abstractmethod
    def visit_assign_expr(self, expr):
        """Visit a Assign node."""
        pass

    @abstractmethod
    def visit_binary_expr(self, expr):
        """Visit a Binary node."""
        pass

    @abstractmethod
    def visit_call_expr(self, expr):
        """Visit a Call node."""
        pass

    @abstractmethod
    def visit_grouping_expr(self, expr):
        """Visit a Grouping node."""
        pass

    @abstractmethod
    def visit_literal_expr(self, expr):
        """Visit a Literal node."""
        pass

    @abstractmethod
    def visit_logical_expr(self, expr):
        """Visit a Logical node."""
        pass

    @abstractmethod
    def visit_unary_expr(self, expr):
        """Visit a Unary node."""
        pass

    @abstractmethod
    def visit_variable_expr(self, expr):
        """Visit a Variable node."""
        pass


class Expr:
    """Expr base class."""

    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor."""
        pass


class Assign(Expr):
    """Assign expression."""

    def __init__(self, name, value):
        """
        Initialize a Assign expression.

        Args:
            name: Token
            value: Expr
        """
        self.name = name
        self.value = value

    def accept(self, visitor):
        """Accept a visitor."""
        return visitor.visit_assign_expr(self)


class Binary(Expr):
    """Binary expression."""

    def __init__(self, left, operator, right):
        """
        Initialize a Binary expression.

        Args:
            left: Expr
            operator: Token
            right: Expr
        """
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        """Accept a visitor."""
        return visitor.visit_binary_expr(self)


class Call(Expr):
    """Call expression."""

    def __init__(self, callee, paren, arguments):
        """
        Initialize a Call expression.

        Args:
            callee: Expr
            paren: Token
            arguments: List<Expr>
        """
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor):
        """Accept a visitor."""
        return visitor.visit_call_expr(self)


class Grouping(Expr):
    """Grouping expression."""

    def __init__(self, expression):
        """
        Initialize a Grouping expression.

        Args:
            expression: Expr
        """
        self.expression = expression

    def accept(self, visitor):
        """Accept a visitor."""
        return visitor.visit_grouping_expr(self)


class Literal(Expr):
    """Literal expression."""

    def __init__(self, value):
        """
        Initialize a Literal expression.

        Args:
            value: object
        """
        self.value = value

    def accept(self, visitor):
        """Accept a visitor."""
        return visitor.visit_literal_expr(self)


class Logical(Expr):
    """Logical expression."""

    def __init__(self, left, operator, right):
        """
        Initialize a Logical expression.

        Args:
            left: Expr
            operator: Token
            right: Expr
        """
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        """Accept a visitor."""
        return visitor.visit_logical_expr(self)


class Unary(Expr):
    """Unary expression."""

    def __init__(self, operator, right):
        """
        Initialize a Unary expression.

        Args:
            operator: Token
            right: Expr
        """
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        """Accept a visitor."""
        return visitor.visit_unary_expr(self)


class Variable(Expr):
    """Variable expression."""

    def __init__(self, name):
        """
        Initialize a Variable expression.

        Args:
            name: Token
        """
        self.name = name

    def accept(self, visitor):
        """Accept a visitor."""
        return visitor.visit_variable_expr(self)


