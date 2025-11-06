"""
AST Printer for the Lox language.
Converts an expression AST back to a string representation.
"""

from expr import Visitor, Expr, Binary, Grouping, Literal, Unary


class AstPrinter(Visitor):
    """Prints an AST in a Lisp-like format."""

    def print(self, expr):
        """
        Print an expression.

        Args:
            expr: The expression to print

        Returns:
            String representation of the expression
        """
        return expr.accept(self)

    def visit_binary_expr(self, expr):
        """Visit a Binary expression."""
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr):
        """Visit a Grouping expression."""
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr):
        """Visit a Literal expression."""
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr):
        """Visit a Unary expression."""
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name, *exprs):
        """
        Wrap expressions in parentheses with a name.

        Args:
            name: The name/operator for this group
            *exprs: Variable number of expressions to wrap

        Returns:
            String like "(name expr1 expr2 ...)"
        """
        parts = ["(", name]
        for expr in exprs:
            parts.append(" ")
            parts.append(expr.accept(self))
        parts.append(")")

        return "".join(parts)


def main():
    """Test the AstPrinter with a sample expression."""
    from TokenType import Token, TokenType

    # Create the expression: (* (- 123) (group 45.67))
    # This represents: -123 * (45.67)
    expression = Binary(
        Unary(
            Token(TokenType.MINUS, "-", None, 1),
            Literal(123)
        ),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(
            Literal(45.67)
        )
    )

    print(AstPrinter().print(expression))


if __name__ == "__main__":
    main()