# Project: Lox Interpreter (Chapters 4-10)

[Overview](#overview)  
[Code Structure](#code-structure)  
[Current Capabilities](#current-capabilities)  
[Limitations](#limitations)  
[Syntax](#syntax)  
[Run and Build](#run-and-build)  
[Testing](#testing)  
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

The interpreter can tokenize source code, parse it into an AST, and execute it with full support for variables, functions, closures, and control flow.

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
  Expression AST node classes (Binary, Unary, Literal, Variable, etc.)

- **`stmt.py`**  
  Statement AST node classes (Print, Var, If, While, Function, etc.)

- **`parser.py`**  
  Recursive descent parser that builds AST from tokens

- **`interpreter.py`**  
  Tree-walk interpreter that executes the AST

- **`environment.py`**  
  Variable storage with support for nested scopes

- **`lox_callable.py`**  
  Abstract interface for callable objects (functions)

- **`lox_function.py`**  
  User-defined function implementation with closure support

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

## Documentation Files

- **`TESTING_GUIDE.md`** - Comprehensive testing instructions
- **`REPL_REFERENCE.md`** - REPL usage guide
- **`COMPLETE_EXPLANATION_PART1-4.md`** - Detailed technical explanation

---

# Current Capabilities

## Lexical Analysis (Chapter 4)
- Tokenization of all Lox constructs
- Number literals (integers and floats)
- String literals with escape sequences
- Identifier recognition
- Keyword detection
- Comment handling (`//`)

## Expression Evaluation (Chapters 5-7)
- Arithmetic operators: `+`, `-`, `*`, `/`
- Comparison operators: `<`, `>`, `<=`, `>=`, `==`, `!=`
- Logical operators: `and`, `or`, `!`
- Unary operators: `-`, `!`
- Grouping with parentheses
- Proper operator precedence and associativity
- String concatenation with `+`

## Variables and State (Chapter 8)
- Variable declarations: `var x = 10;`
- Uninitialized variables (default to `nil`)
- Variable assignment: `x = 5;`
- Block scoping with `{ }`
- Variable shadowing
- Nested scopes with proper environment chains

## Control Flow (Chapter 9)
- **If statements**: `if (condition) statement else statement`
- **While loops**: `while (condition) statement`
- **For loops**: `for (init; condition; increment) statement`
- **Logical operators with short-circuit evaluation**:
  - `and` - stops on first false
  - `or` - stops on first true
- Nested control structures

## Functions (Chapter 10)
- **Function declarations**: `fun name(params) { body }`
- **Function calls**: `function(args)`
- **Return statements**: `return value;`
- **First-class functions**: Pass as arguments, return from functions
- **Closures**: Functions capture their surrounding scope
- **Recursion**: Full support for recursive functions
- **Higher-order functions**: Functions that take/return functions
- **Native functions**: `clock()` returns current timestamp
- Up to 255 parameters per function

## Type System
- **Numbers**: Double-precision floating point
- **Strings**: Immutable text with concatenation
- **Booleans**: `true`, `false`
- **Nil**: `nil` (null/none equivalent)
- **Functions**: First-class callable objects

## Error Handling
- Lexical errors (invalid characters, unterminated strings)
- Parse errors with error recovery
- Runtime errors (undefined variables, type errors)
- REPL resilience (errors don't crash REPL)

---

# Limitations

## Not Implemented (Chapters 11-13)
- **Static variable resolution** (Chapter 11)
- **Classes and objects** (Chapter 12)
- **Inheritance** (Chapter 13)

## Language Restrictions
- No break/continue statements
- No switch/case statements
- No exception handling (try/catch)
- No imports/modules
- Limited standard library (only `clock()`)

## Implementation Details
- No garbage collection 
- No optimization 
- Limited error messages compared to production languages

---

# Syntax

## Variable Declarations
```lox
// Declaration with initializer
var x = 10;
var message = "hello";
var truth = true;

// Uninitialized (defaults to nil)
var y;

// Assignment
x = 20;
y = x + 5;
```

## Control Flow

### If Statements
```lox
// Simple if
if (x > 10) print "large";

// If-else
if (x > 10) {
  print "large";
} else {
  print "small";
}

// Nested if
if (x > 10) {
  if (x > 20) {
    print "very large";
  }
}
```

### While Loops
```lox
var i = 0;
while (i < 5) {
  print i;
  i = i + 1;
}
```

### For Loops
```lox
// Standard for loop
for (var i = 0; i < 5; i = i + 1) {
  print i;
}

// Infinite loop
for (;;) {
  print "forever";
}

// No initializer
var j = 0;
for (; j < 3; j = j + 1) {
  print j;
}
```

### Logical Operators
```lox
// Short-circuit AND
if (x != nil and x > 10) {
  print "valid and large";
}

// Short-circuit OR
var value = input() or "default";

// NOT
if (!isDone) {
  print "still working";
}
```

## Functions

### Function Declaration
```lox
// Simple function
fun greet(name) {
  print "Hello, " + name + "!";
}

// Function with return
fun add(a, b) {
  return a + b;
}

// Multiple parameters
fun multiply(a, b, c) {
  return a * b * c;
}

// No parameters
fun sayHello() {
  print "Hello!";
}
```

### Recursive Functions
```lox
// Factorial
fun factorial(n) {
  if (n <= 1) return 1;
  return n * factorial(n - 1);
}

// Fibonacci
fun fib(n) {
  if (n <= 1) return n;
  return fib(n - 2) + fib(n - 1);
}
```

### Closures
```lox
// Counter closure
fun makeCounter() {
  var count = 0;
  fun counter() {
    count = count + 1;
    return count;
  }
  return counter;
}

var c = makeCounter();
print c();  // 1
print c();  // 2
print c();  // 3

// Adder factory
fun makeAdder(n) {
  fun adder(x) {
    return x + n;
  }
  return adder;
}

var add5 = makeAdder(5);
print add5(3);  // 8
```

### Higher-Order Functions
```lox
// Function that takes a function
fun twice(fn, x) {
  return fn(fn(x));
}

fun double(n) {
  return n * 2;
}

print twice(double, 5);  // 20
```

## Block Scoping
```lox
var x = "global";

{
  var x = "local";
  print x;  // local
}

print x;  // global
```

## Native Functions
```lox
// Get current Unix timestamp
var start = clock();
// ... do work ...
var end = clock();
print "Elapsed: " + (end - start);
```

---

# Run and Build

## Prerequisites
- Python 3.7 or higher
- No external dependencies required

## Running the Interpreter

### REPL (Interactive Mode)
```bash
python3 lox.py
```

Then type Lox code interactively:
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
python3 lox.py test_comprehensive.lox
```

## Running Tests

### Run All Tests
```bash
python3 run_tests.py
```

### Run Individual Tests
```bash
python3 lox.py test_chapter4_scanning.lox
python3 lox.py test_chapter6_expressions.lox
python3 lox.py test_chapter7_evaluation.lox
python3 lox.py test_chapter8_statements.lox
python3 lox.py test_chapter9_control.lox
python3 lox.py test_chapter10_functions.lox
python3 lox.py test_comprehensive.lox
```

## Regenerating AST Classes
If you modify the AST definitions:
```bash
python3 GenerateAST.py .
```

This regenerates `expr.py` and `stmt.py`.

---

# Testing

## Test Coverage

### Chapter 4: Scanning (~90 lines)
Tests all token types:
- Numbers, strings, identifiers, keywords
- All operators
- Comments
- Whitespace handling

**Expected Output**: Confirms all tokens recognized

### Chapter 6: Expressions (~90 lines)
Tests expression parsing:
- Literals
- Unary/binary operators
- Operator precedence
- Grouping
- String concatenation

**Expected Output**: All expressions evaluate correctly

### Chapter 7: Evaluation (~80 lines)
Tests runtime evaluation:
- Truthiness rules
- Arithmetic operations
- Comparisons
- Nested expressions

**Expected Output**: Correct evaluation results

### Chapter 8: Statements (~100 lines)
Tests variables and scoping:
- Variable declarations
- Assignment
- Block scopes
- Variable shadowing
- Nested blocks

**Expected Output**: Proper scoping behavior

### Chapter 9: Control Flow (~130 lines)
Tests control structures:
- If/else statements
- Logical operators (and, or)
- While loops
- For loops
- Nested control flow

**Expected Output**: Correct branching and looping

### Chapter 10: Functions 
Tests functions and closures:
- Function declarations
- Function calls
- Return statements
- Recursion (fibonacci, factorial)
- Closures (counter, adder factory)
- Higher-order functions
- Native functions

**Expected Output**: All function features work

### Comprehensive Test (~160 lines)
Integration test with real-world examples:
- Bank account simulation (closures)
- FizzBuzz-like pattern
- All features combined

**Expected Output**: Complete working language

# Conclusion

This project successfully demonstrates a working Lox interpreter with support for:

✅ **Complete lexical analysis** - All token types recognized  
✅ **Recursive descent parsing** - Proper precedence and associativity  
✅ **Expression evaluation** - Arithmetic, logical, and comparison operations  
✅ **Variables and scoping** - Block scopes with proper environment chains  
✅ **Control flow** - If/else, while, for, with short-circuit evaluation  
✅ **Functions** - First-class functions with parameters and returns  
✅ **Closures** - Functions capture their lexical environment  
✅ **Recursion** - Full support for recursive algorithms  
✅ **Error handling** - Graceful error recovery in REPL  


## Future Enhancements (Chapters 11-13)

Potential additions to reach 100%:
- **Chapter 11**: Static variable resolution and semantic analysis
- **Chapter 12**: Classes, methods, and instances
- **Chapter 13**: Inheritance and superclasses

---