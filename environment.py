"""
Environment for storing variables in the Lox interpreter.
"""

from Interpreter import RuntimeError as LoxRuntimeError


class Environment:
    """Stores variable bindings."""

    def __init__(self, enclosing=None):
        """
        Initialize an environment.

        Args:
            enclosing: Parent environment for nested scopes
        """
        self.enclosing = enclosing
        self.values = {}

    def define(self, name, value):
        """
        Define a new variable.

        Args:
            name: Variable name (string)
            value: Variable value
        """
        self.values[name] = value

    def get(self, name):
        """
        Get the value of a variable.

        Args:
            name: Token representing the variable name

        Returns:
            The variable's value

        Raises:
            RuntimeError: If variable is undefined
        """
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        # If not found in this environment, try the enclosing one
        if self.enclosing is not None:
            return self.enclosing.get(name)

        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def assign(self, name, value):
        """
        Assign a value to an existing variable.

        Args:
            name: Token representing the variable name
            value: The new value

        Raises:
            RuntimeError: If variable is undefined
        """
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        # If not found in this environment, try the enclosing one
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return

        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")