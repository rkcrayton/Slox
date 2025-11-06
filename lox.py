#!/usr/bin/env python3
"""
Lox Interpreter
Based on Crafting Interpreters by Robert Nystrom
"""

import sys
from Scanner import Scanner
from Parser import Parser
from Interpreter import Interpreter


class Lox:
    """Main Lox interpreter class."""

    had_error = False
    had_runtime_error = False
    interpreter = None

    def __init__(self):
        pass

    @staticmethod
    def main(args):
        """Main entry point for the Lox interpreter."""
        # Initialize the interpreter
        Lox.interpreter = Interpreter()

        if len(args) > 1:
            print("Usage: jlox [script]")
            sys.exit(64)
        elif len(args) == 1:
            Lox.run_file(args[0])
        else:
            Lox.run_prompt()

    @staticmethod
    def run_file(path):
        """Run a Lox script from a file."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                source = f.read()
            Lox.run(source)

            # Indicate an error in the exit code.
            if Lox.had_error:
                sys.exit(65)
            if Lox.had_runtime_error:
                sys.exit(70)
        except IOError as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(74)

    @staticmethod
    def run_prompt():
        """Run the Lox REPL (Read-Eval-Print Loop)."""
        print("Lox REPL - Enter Lox code (Ctrl+D or Ctrl+C to exit)")
        try:
            while True:
                try:
                    line = input("> ")
                    if line:
                        Lox.run(line)
                        Lox.had_error = False
                except EOFError:
                    print("\nExiting...")
                    break
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)

    @staticmethod
    def run(source):
        """Run Lox source code."""
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()

        # Stop if there was a syntax error.
        if Lox.had_error:
            return

        if expression is not None:
            Lox.interpreter.interpret(expression)

    @staticmethod
    def error(line, message):
        """Report an error at a given line."""
        Lox.report(line, "", message)

    @staticmethod
    def error_token(token, message):
        """Report an error at a given token."""
        from TokenType import TokenType
        if token.type == TokenType.EOF:
            Lox.report(token.line, " at end", message)
        else:
            Lox.report(token.line, f" at '{token.lexeme}'", message)

    @staticmethod
    def runtime_error(error):
        """Report a runtime error."""
        print(f"{error}\n[line {error.token.line}]", file=sys.stderr)
        Lox.had_runtime_error = True

    @staticmethod
    def report(line, where, message):
        """Report an error with location information."""
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
        Lox.had_error = True


if __name__ == "__main__":
    Lox.main(sys.argv[1:])