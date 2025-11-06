#!/usr/bin/env python3
"""
Test suite for Lox scanner, AST, and printer.
"""

from Scanner import Scanner
from TokenType import Token, TokenType
from expr import Binary, Grouping, Literal, Unary
from astprinter import AstPrinter


def test_scanner():
    """Test the scanner with various inputs."""
    print("=" * 60)
    print("TESTING SCANNER")
    print("=" * 60)

    test_cases = [
        ("1 + 2", "Simple addition"),
        ("(1 + 2) * 3", "Grouping and operators"),
        ("-123.45", "Negative decimal"),
        ("!true", "Unary not"),
        ('"hello world"', "String literal"),
        ("var x = 10;", "Variable declaration"),
        ("if (x > 5) { print x; }", "If statement"),
        ("// comment\n1 + 2", "Comment handling"),
    ]

    for source, description in test_cases:
        print(f"\n{description}: {source}")
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        print(f"  Tokens: {len(tokens)}")
        for token in tokens:
            if token.type != TokenType.EOF:
                print(f"    {token}")


def test_ast_creation():
    """Test creating AST nodes manually."""
    print("\n" + "=" * 60)
    print("TESTING AST CREATION")
    print("=" * 60)

    # Test 1: Simple literal
    print("\nTest 1: Literal(42)")
    expr1 = Literal(42)
    print(f"  Created: {expr1}")
    print(f"  Type: {type(expr1).__name__}")

    # Test 2: Unary expression
    print("\nTest 2: Unary(-123)")
    expr2 = Unary(
        Token(TokenType.MINUS, "-", None, 1),
        Literal(123)
    )
    print(f"  Created: Unary with operator '{expr2.operator.lexeme}'")

    # Test 3: Binary expression
    print("\nTest 3: Binary(1 + 2)")
    expr3 = Binary(
        Literal(1),
        Token(TokenType.PLUS, "+", None, 1),
        Literal(2)
    )
    print(f"  Created: Binary with operator '{expr3.operator.lexeme}'")

    # Test 4: Complex nested expression
    print("\nTest 4: Complex((1 + 2) * 3)")
    expr4 = Binary(
        Grouping(
            Binary(
                Literal(1),
                Token(TokenType.PLUS, "+", None, 1),
                Literal(2)
            )
        ),
        Token(TokenType.STAR, "*", None, 1),
        Literal(3)
    )
    print(f"  Created: Complex nested binary expression")


def test_ast_printer():
    """Test the AST printer with various expressions."""
    print("\n" + "=" * 60)
    print("TESTING AST PRINTER")
    print("=" * 60)

    printer = AstPrinter()

    test_cases = [
        (
            Literal(42),
            "42",
            "Simple literal"
        ),
        (
            Unary(
                Token(TokenType.MINUS, "-", None, 1),
                Literal(123)
            ),
            "(- 123)",
            "Unary negation"
        ),
        (
            Binary(
                Literal(1),
                Token(TokenType.PLUS, "+", None, 1),
                Literal(2)
            ),
            "(+ 1 2)",
            "Binary addition"
        ),
        (
            Binary(
                Unary(
                    Token(TokenType.MINUS, "-", None, 1),
                    Literal(123)
                ),
                Token(TokenType.STAR, "*", None, 1),
                Grouping(Literal(45.67))
            ),
            "(* (- 123) (group 45.67))",
            "Complex expression from book"
        ),
        (
            Binary(
                Binary(
                    Literal(1),
                    Token(TokenType.PLUS, "+", None, 1),
                    Literal(2)
                ),
                Token(TokenType.STAR, "*", None, 1),
                Binary(
                    Literal(3),
                    Token(TokenType.MINUS, "-", None, 1),
                    Literal(4)
                )
            ),
            "(* (+ 1 2) (- 3 4))",
            "Nested binary operations"
        ),
    ]

    for expr, expected, description in test_cases:
        result = printer.print(expr)
        status = "✓" if result == expected else "✗"
        print(f"\n{status} {description}")
        print(f"  Expected: {expected}")
        print(f"  Got:      {result}")
        if result != expected:
            print("  ERROR: Mismatch!")


def test_visitor_pattern():
    """Test that the visitor pattern works correctly."""
    print("\n" + "=" * 60)
    print("TESTING VISITOR PATTERN")
    print("=" * 60)

    # Create a simple expression
    expr = Binary(
        Literal(1),
        Token(TokenType.PLUS, "+", None, 1),
        Literal(2)
    )

    # Test that accept() properly dispatches to visitor
    printer = AstPrinter()
    result = expr.accept(printer)

    print(f"\nExpression: 1 + 2")
    print(f"Visitor result: {result}")
    print(f"Direct print: {printer.print(expr)}")

    if result == "(+ 1 2)":
        print("✓ Visitor pattern working correctly!")
    else:
        print("✗ Visitor pattern failed!")


def test_edge_cases():
    """Test edge cases and special values."""
    print("\n" + "=" * 60)
    print("TESTING EDGE CASES")
    print("=" * 60)

    printer = AstPrinter()

    # Test nil
    print("\nTest: nil literal")
    expr = Literal(None)
    result = printer.print(expr)
    print(f"  Result: {result}")
    print(f"  Expected: nil")
    print(f"  Status: {'✓' if result == 'nil' else '✗'}")

    # Test string
    print("\nTest: String literal")
    expr = Literal("hello")
    result = printer.print(expr)
    print(f"  Result: {result}")
    print(f"  Expected: hello")
    print(f"  Status: {'✓' if result == 'hello' else '✗'}")

    # Test boolean
    print("\nTest: Boolean literal")
    expr = Literal(True)
    result = printer.print(expr)
    print(f"  Result: {result}")
    print(f"  Expected: True")
    print(f"  Status: {'✓' if result == 'True' else '✗'}")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("LOX INTERPRETER TEST SUITE")
    print("=" * 60)

    try:
        test_scanner()
        test_ast_creation()
        test_ast_printer()
        test_visitor_pattern()
        test_edge_cases()

        print("\n" + "=" * 60)
        print("ALL TESTS COMPLETED")
        print("=" * 60)

    except Exception as e:
        print(f"\n\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()