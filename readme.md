# Project: Lox Interpreter (Chapters 4-10)

[Overview](#overview)  
[Code Structure](#code-structure)  
[Current Capabilities](#current-capabilities)  
[Limitations](#limitations)
[Run and Build](#run-and-build)
[Conclusion](#conclusion)
---

# Overview

This project implements a complete Lox interpreter in Python following "Crafting Interpreters" by Robert Nystrom. The implementation covers Chapters 4-10, building a fully functional, Turing-complete programming language with:

- **Chapter 4**: Lexical analysis (scanning) - Converting source code into tokens
- **Chapter 5**: Abstract Syntax Tree (AST) representation of code
- **Chapter 6**: Parsing expressions with proper operator precedence
- **Chapter 7**: Expression evaluation and runtime execution
- **Chapter 8**: Variables, assignment, and block scoping
- **Chapter 9**: Control flow (if/else, while, for loops, logical operators)
- **Chapter 10**: Functions, closures, and return statements

---

# Code Structure

## Core Files

- **`lox.py`**  
  Main entry point with REPL, file execution, and error handling

- **`token_type.py`**  
  Defines `TokenType` enum and `Token` class for all Lox token types

- **`scanner.py`**  
  Lexical analyzer that converts source code into tokens

- **`expr.py`**  
  Expression AST node classes

- **`stmt.py`**  
  Statement AST node classes

- **`parser.py`**  
  Recursive descent parser that builds AST from tokens

- **`interpreter.py`**  
  Tree-walk interpreter that executes the AST

- **`environment.py`**  
  Variable storage with support for nested scopes

- **`lox_callable.py`**  
  Abstract interface for callable objects (functions)

- **`lox_function.py`**  
  User-defined function implementation

- **`return_exception.py`**  
  Exception-based control flow for return statements

- **`generate_ast.py`**  
  Code generator that creates `expr.py` and `stmt.py` from specifications

## Test Files

- **`test_chapter4_scanning.lox`** - Tests all token types
- **`test_chapter6_expressions.lox`** - Tests expression parsing
- **`test_chapter7_evaluation.lox`** - Tests expression evaluation
- **`test_chapter8_statements.lox`** - Tests variables and scoping
- **`test_chapter9_control.lox`** - Tests control flow
- **`test_chapter10_functions.lox`** - Tests functions and closures
- **`test_comprehensive.lox`** - Complete integration test
- **`run_tests.py`** - Automated test runner

---

# Current Capabilities

## Lexical Analysis (Chapter 4)
- Tokenization of all Lox constructs
- Number literals (integers and floats)
- String literals
- Keyword detection
- Comment handling (`//`)

## Expression Evaluation (Chapters 5-7)
- Arithmetic operators: `+`, `-`, `*`, `/`
- Comparison operators: `<`, `>`, `<=`, `>=`, `==`, `!=`
- Logical operators: `and`, `or`, `!`
- Unary operators: `-`, `!`
- Grouping with parentheses
- String concatenation with `+`

## Variables and State (Chapter 8)
- Variable declarations: `var x = 10;`
- Uninitialized variables (default to `nil`)
- Variable assignment: `x = 5;`
- Block scoping with `{ }`

## Control Flow (Chapter 9)
- **If statements**: `if (condition) statement else statement`
- **While loops**: `while (condition) statement`
- **For loops**: `for (init; condition; increment) statement`
- **Logical operators with short-circuit evaluation**:
  - `and` - stops on first false
  - `or` - stops on first true

## Functions (Chapter 10)
- **Function declarations**: `fun name(params) { body }`
- **Function calls**: `function(args)`
- **Return statements**: `return value;`
- **First-class functions**: Pass as arguments, return from functions
- **Closures**: Functions capture their surrounding scope
- **Recursion**: Full support for recursive functions
- **Native functions**: `clock()` returns current timestamp

## Error Handling
- Lexical errors 
- Parse errors with error recovery
- Runtime errors 

---

# Limitations

## Not Implemented (Chapters 11-13)
- **Resolving and Binding** (Chapter 11)
- **Classes** (Chapter 12)
- **Inheritance** (Chapter 13)

## Language Restrictions
- No imports/modules
- Limited standard library (only `clock()`)

---

# Run and Build

## Running the Interpreter

### REPL 
```bash
python3 lox.py
```

Then type Lox code :
```
> var x = 10;
> print x + 5;
15
> fun double(n) { return n * 2; }
> print double(x);
20
> Ctrl+D to exit
```

### Execute a File
```bash
python3 lox.py filename.lox
```

Example:
```bash
python3 lox.py test/test_chapter4_scanning.lox
```

## Running Tests

### Run All Tests
```bash
python3 run_test.py
```

### Run Individual Tests
```bash
python3 lox.py test/test_chapter4_scanning.lox
python3 lox.py test/test_chapter6_expressions.lox
python3 lox.py test/test_chapter7_evaluation.lox
python3 lox.py test/test_chapter8_statements.lox
python3 lox.py test/test_chapter9_control.lox
python3 lox.py test/test_chapter10_functions.lox
python3 lox.py test/quick_sort.lox
python3 lox.py test/insertion_sort.lox
python3 lox.py test/merge_sort.lox
python3 lox.py test/BankAccount.lox
python3 lox.py test/fib.lox
```

## Regenerating AST Classes
If you modify the AST definitions:
```bash
python3 GenerateAST.py .
```

This regenerates `expr.py` and `stmt.py`.

# Conclusion

This project successfully demonstrates a working Lox interpreter with support for:

**Complete lexical analysis** - All token types recognized  
**Recursive descent parsing** - Proper precedence and associativity  
**Expression evaluation** - Arithmetic, logical, and comparison operations  
**Variables and scoping** - Block scopes with proper environment chains  
**Control flow** - If/else, while, for, with short-circuit evaluation  
**Functions** - First-class functions with parameters and returns
**Error handling** - Graceful error recovery in REPL  
