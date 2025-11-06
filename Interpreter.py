"""
Interpreter for the Lox language.
Evaluates the Abstract Syntax Tree.
"""

from expr import Visitor as ExprVisitor, Binary, Grouping, Literal, Unary
from stmt import Visitor as StmtVisitor
from TokenType import TokenType


class RuntimeError(Exception):
    """Runtime error during interpretation."""

    def __init__(self, token, message):
        super().__init__(message)
        self.token = token


class Interpreter(ExprVisitor, StmtVisitor):
    """Interprets and evaluates Lox expressions and statements."""

    def __init__(self):
        """Initialize the interpreter with an empty environment."""
        from environment import Environment
        self.environment = Environment()

    def interpret(self, statements):
        """
        Interpret a list of statements.

        Args:
            statements: List of statements to execute
        """
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError as error:
            from lox import Lox
            Lox.runtime_error(error)

    def execute(self, stmt):
        """
        Execute a statement.

        Args:
            stmt: The statement to execute
        """
        stmt.accept(self)

    def visit_expression_stmt(self, stmt):
        """
        Execute an expression statement.

        Args:
            stmt: Expression statement
        """
        self.evaluate(stmt.expression)
        return None

    def visit_print_stmt(self, stmt):
        """
        Execute a print statement.

        Args:
            stmt: Print statement
        """
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None

    def visit_var_stmt(self, stmt):
        """
        Execute a variable declaration statement.

        Args:
            stmt: Var statement
        """
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)
        return None

    def visit_block_stmt(self, stmt):
        """
        Execute a block statement.

        Args:
            stmt: Block statement
        """
        from environment import Environment
        self.execute_block(stmt.statements, Environment(self.environment))
        return None

    def visit_if_stmt(self, stmt):
        """
        Execute an if statement.

        Args:
            stmt: If statement
        """
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.thenBranch)
        elif stmt.elseBranch is not None:
            self.execute(stmt.elseBranch)
        return None

    def visit_while_stmt(self, stmt):
        """
        Execute a while statement.

        Args:
            stmt: While statement
        """
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
        return None

    def execute_block(self, statements, environment):
        """
        Execute a list of statements in a given environment.

        Args:
            statements: List of statements to execute
            environment: The environment for this block
        """
        previous = self.environment
        try:
            self.environment = environment

            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def visit_variable_expr(self, expr):
        """
        Evaluate a variable expression.

        Args:
            expr: Variable expression

        Returns:
            The variable's value
        """
        return self.environment.get(expr.name)

    def visit_assign_expr(self, expr):
        """
        Evaluate an assignment expression.

        Args:
            expr: Assign expression

        Returns:
            The assigned value
        """
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visit_logical_expr(self, expr):
        """
        Evaluate a logical expression.

        Args:
            expr: Logical expression

        Returns:
            The result of the logical operation
        """
        left = self.evaluate(expr.left)

        # Short-circuit evaluation
        if expr.operator.type == TokenType.OR:
            if self.is_truthy(left):
                return left
        else:  # AND
            if not self.is_truthy(left):
                return left

        return self.evaluate(expr.right)

    def visit_literal_expr(self, expr):
        """
        Evaluate a literal expression.

        Args:
            expr: Literal expression

        Returns:
            The literal value
        """
        return expr.value

    def visit_grouping_expr(self, expr):
        """
        Evaluate a grouping expression.

        Args:
            expr: Grouping expression

        Returns:
            The value of the inner expression
        """
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr):
        """
        Evaluate a unary expression.

        Args:
            expr: Unary expression

        Returns:
            The result of applying the unary operator
        """
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            self.check_number_operand(expr.operator, right)
            return -float(right)
        elif expr.operator.type == TokenType.BANG:
            return not self.is_truthy(right)

        # Unreachable
        return None

    def visit_binary_expr(self, expr):
        """
        Evaluate a binary expression.

        Args:
            expr: Binary expression

        Returns:
            The result of applying the binary operator
        """
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        operator_type = expr.operator.type

        # Arithmetic operators
        if operator_type == TokenType.MINUS:
            self.check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
        elif operator_type == TokenType.SLASH:
            self.check_number_operands(expr.operator, left, right)
            return float(left) / float(right)
        elif operator_type == TokenType.STAR:
            self.check_number_operands(expr.operator, left, right)
            return float(left) * float(right)
        elif operator_type == TokenType.PLUS:
            # Addition for numbers, concatenation for strings
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
            raise RuntimeError(expr.operator,
                             "Operands must be two numbers or two strings.")

        # Comparison operators
        elif operator_type == TokenType.GREATER:
            self.check_number_operands(expr.operator, left, right)
            return float(left) > float(right)
        elif operator_type == TokenType.GREATER_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)
        elif operator_type == TokenType.LESS:
            self.check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        elif operator_type == TokenType.LESS_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)

        # Equality operators
        elif operator_type == TokenType.BANG_EQUAL:
            return not self.is_equal(left, right)
        elif operator_type == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)

        # Unreachable
        return None

    def evaluate(self, expr):
        """
        Evaluate an expression by accepting this visitor.

        Args:
            expr: The expression to evaluate

        Returns:
            The value of the expression
        """
        return expr.accept(self)

    def is_truthy(self, obj):
        """
        Determine the truthiness of a value.
        In Lox: nil and false are falsey, everything else is truthy.

        Args:
            obj: The value to check

        Returns:
            bool: True if truthy, False if falsey
        """
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def is_equal(self, a, b):
        """
        Check equality between two values.

        Args:
            a: First value
            b: Second value

        Returns:
            bool: True if equal, False otherwise
        """
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b

    def check_number_operand(self, operator, operand):
        """
        Check that an operand is a number.

        Args:
            operator: The operator token
            operand: The operand to check

        Raises:
            RuntimeError: If operand is not a number
        """
        if isinstance(operand, float):
            return
        raise RuntimeError(operator, "Operand must be a number.")

    def check_number_operands(self, operator, left, right):
        """
        Check that both operands are numbers.

        Args:
            operator: The operator token
            left: Left operand
            right: Right operand

        Raises:
            RuntimeError: If operands are not numbers
        """
        if isinstance(left, float) and isinstance(right, float):
            return
        raise RuntimeError(operator, "Operands must be numbers.")

    def stringify(self, obj):
        """
        Convert a Lox value to a string for printing.

        Args:
            obj: The value to convert

        Returns:
            str: String representation
        """
        if obj is None:
            return "nil"

        if isinstance(obj, float):
            text = str(obj)
            # Remove trailing .0 for whole numbers
            if text.endswith(".0"):
                text = text[:-2]
            return text

        if isinstance(obj, bool):
            return "true" if obj else "false"

        return str(obj)