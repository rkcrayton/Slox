#!/usr/bin/env python3

import sys


def main():
    if len(sys.argv) != 2:
        print("Usage: generate_ast <output directory>")
        sys.exit(64)

    output_dir = sys.argv[1]

    define_ast(output_dir, "Expr", [
        "Assign   : Token name, Expr value",
        "Binary   : Expr left, Token operator, Expr right",
        "Call     : Expr callee, Token paren, List<Expr> arguments",
        "Grouping : Expr expression",
        "Literal  : object value",
        "Logical  : Expr left, Token operator, Expr right",
        "Unary    : Token operator, Expr right",
        "Variable : Token name"
    ])

    define_ast(output_dir, "Stmt", [
        "Block      : List<Stmt> statements",
        "Expression : Expr expression",
        "Function   : Token name, List<Token> params, List<Stmt> body",
        "If         : Expr condition, Stmt thenBranch, Stmt elseBranch",
        "Print      : Expr expression",
        "Return     : Token keyword, Expr value",
        "Var        : Token name, Expr initializer",
        "While      : Expr condition, Stmt body"
    ])


def define_ast(output_dir, base_name, types):
    path = f"{output_dir}/{base_name.lower()}.py"

    with open(path, 'w') as writer:
        writer.write('from TokenType import Token\n')
        writer.write('from abc import ABC, abstractmethod\n\n')

        # Write the Visitor interface
        define_visitor(writer, base_name, types)

        # Write the base class
        writer.write(f'class {base_name}:\n')
        writer.write(f'    """{base_name} base class."""\n\n')
        writer.write('    @abstractmethod\n')
        writer.write('    def accept(self, visitor):\n')
        writer.write('        """Accept a visitor."""\n')
        writer.write('        pass\n\n\n')

        # Write each subclass
        for type_def in types:
            class_name = type_def.split(':')[0].strip()
            fields = type_def.split(':')[1].strip()
            define_type(writer, base_name, class_name, fields)


def define_visitor(writer, base_name, types):
    writer.write('class Visitor(ABC):\n')
    writer.write('    """Visitor interface for AST traversal."""\n\n')

    for type_def in types:
        type_name = type_def.split(':')[0].strip()
        writer.write('    @abstractmethod\n')
        writer.write(f'    def visit_{type_name.lower()}_{base_name.lower()}(self, {base_name.lower()}):\n')
        writer.write(f'        """Visit a {type_name} node."""\n')
        writer.write('        pass\n\n')

    writer.write('\n')


def define_type(writer, base_name, class_name, field_list):
    writer.write(f'class {class_name}({base_name}):\n')
    writer.write(f'    """{class_name} expression."""\n\n')

    # Parse fields
    if field_list:
        fields = [field.strip() for field in field_list.split(',')]
        field_names = [field.split()[1] for field in fields]

        # Constructor
        writer.write(f'    def __init__(self, {", ".join(field_names)}):\n')
        writer.write('        """\n')
        writer.write(f'        Initialize a {class_name} expression.\n\n')
        writer.write('        Args:\n')
        for field in fields:
            parts = field.split()
            type_name = parts[0]
            field_name = parts[1]
            writer.write(f'            {field_name}: {type_name}\n')
        writer.write('        """\n')

        # Store parameters in fields
        for field_name in field_names:
            writer.write(f'        self.{field_name} = {field_name}\n')
    else:
        writer.write('    def __init__(self):\n')
        writer.write(f'        """Initialize a {class_name} expression."""\n')
        writer.write('        pass\n')

    # Visitor pattern
    writer.write('\n')
    writer.write('    def accept(self, visitor):\n')
    writer.write('        """Accept a visitor."""\n')
    writer.write(f'        return visitor.visit_{class_name.lower()}_{base_name.lower()}(self)\n')

    writer.write('\n\n')


if __name__ == "__main__":
    main()