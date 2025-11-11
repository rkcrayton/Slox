

from expr import Visitor as ExprVisitor, Binary, Grouping, Literal, Unary
from stmt import Visitor as StmtVisitor
from TokenType import TokenType
from lox_callable import LoxCallable
import time


class Clock(LoxCallable):

    def arity(self):
        return 0

    def call(self, interpreter, arguments):
        return time.time()

    def __str__(self):
        return "<native fn>"


class RuntimeError(Exception):

    def __init__(self, token, message):
        super().__init__(message)
        self.token = token


class Interpreter(ExprVisitor, StmtVisitor):

    def __init__(self):
        from environment import Environment
        self.globals = Environment()
        self.environment = self.globals

        # Define native functions
        self.globals.define("clock", Clock())

    def interpret(self, statements):
        try:
            for statement in statements:
                if statement is not None:  # Skip None from parse errors
                    self.execute(statement)
        except RuntimeError as error:
            from lox import Lox
            Lox.runtime_error(error)

    def execute(self, stmt):
        stmt.accept(self)

    def visit_expression_stmt(self, stmt):
        self.evaluate(stmt.expression)
        return None

    def visit_print_stmt(self, stmt):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None

    def visit_var_stmt(self, stmt):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)
        return None

    def visit_block_stmt(self, stmt):
        from environment import Environment
        self.execute_block(stmt.statements, Environment(self.environment))
        return None

    def visit_if_stmt(self, stmt):
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.thenBranch)
        elif stmt.elseBranch is not None:
            self.execute(stmt.elseBranch)
        return None

    def visit_while_stmt(self, stmt):
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
        return None

    def visit_function_stmt(self, stmt):
        from lox_function import LoxFunction

        # Capture the current environment as the closure
        function = LoxFunction(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, function)
        return None

    def visit_return_stmt(self, stmt):
        from return_exception import Return

        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)

        raise Return(value)

    def execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment

            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def visit_variable_expr(self, expr):
        return self.environment.get(expr.name)

    def visit_assign_expr(self, expr):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visit_logical_expr(self, expr):
        left = self.evaluate(expr.left)

        # Short-circuit evaluation
        if expr.operator.type == TokenType.OR:
            if self.is_truthy(left):
                return left
        else:  # AND
            if not self.is_truthy(left):
                return left

        return self.evaluate(expr.right)

    def visit_call_expr(self, expr):
        from lox_callable import LoxCallable

        callee = self.evaluate(expr.callee)

        arguments = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))

        if not isinstance(callee, LoxCallable):
            raise RuntimeError(expr.paren, "Can only call functions and classes.")

        function = callee

        if len(arguments) != function.arity():
            raise RuntimeError(expr.paren,
                f"Expected {function.arity()} arguments but got {len(arguments)}.")

        return function.call(self, arguments)

    def visit_literal_expr(self, expr):
        return expr.value

    def visit_grouping_expr(self, expr):
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr):
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            self.check_number_operand(expr.operator, right)
            return -float(right)
        elif expr.operator.type == TokenType.BANG:
            return not self.is_truthy(right)

        # Unreachable
        return None

    def visit_binary_expr(self, expr):
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
        return expr.accept(self)

    def is_truthy(self, obj):
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def is_equal(self, a, b):
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b

    def check_number_operand(self, operator, operand):
        if isinstance(operand, float):
            return
        raise RuntimeError(operator, "Operand must be a number.")

    def check_number_operands(self, operator, left, right):
        if isinstance(left, float) and isinstance(right, float):
            return
        raise RuntimeError(operator, "Operands must be numbers.")

    def stringify(self, obj):
        if obj is None:
            return "nil"

        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[:-2]
            return text

        if isinstance(obj, bool):
            return "true" if obj else "false"

        return str(obj)