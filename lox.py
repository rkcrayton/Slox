#!/usr/bin/env python3

import sys
from Scanner import Scanner
from Parser import Parser
from Interpreter import Interpreter


class Lox:

    had_error = False
    had_runtime_error = False
    interpreter = None

    def __init__(self):
        pass

    @staticmethod
    def main(args):
        # Initialize the interpreter
        Lox.interpreter = Interpreter()

        if len(args) > 1:
            print("Usage: jlox [script]")
            sys.exit(64)
        elif len(args) == 1:
            Lox.run_file(args[0])
        else:
            Lox.run_prompt()


# run file directly
    @staticmethod
    def run_file(path):
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

# Run code within prompt
    @staticmethod
    def run_prompt():
        print("Lox REPL - Enter Lox code (Ctrl+D or Ctrl+C to exit)")
        try:
            while True:
                try:
                    line = input("> ")
                    if line:
                        Lox.run(line)
                        # Reset error flags so errors don't stop the REPL
                        Lox.had_error = False
                        Lox.had_runtime_error = False
                except EOFError:
                    print("\nExiting...")
                    break
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)


# Run Lox code
    @staticmethod
    def run(source):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        statements = parser.parse()

        # Stop if there was a syntax error.
        if Lox.had_error:
            return

        Lox.interpreter.interpret(statements)

# Report errors
    @staticmethod
    def error(line, message):
        Lox.report(line, "", message)

# Report error tokens
    @staticmethod
    def error_token(token, message):
        from TokenType import TokenType
        if token.type == TokenType.EOF:
            Lox.report(token.line, " at end", message)
        else:
            Lox.report(token.line, f" at '{token.lexeme}'", message)

# Runntime error
    @staticmethod
    def runtime_error(error):
        print(f"{error}\n[line {error.token.line}]", file=sys.stderr)
        Lox.had_runtime_error = True

# Report error location
    @staticmethod
    def report(line, where, message):
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
        Lox.had_error = True


if __name__ == "__main__":
    Lox.main(sys.argv[1:])