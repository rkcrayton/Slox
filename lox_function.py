

from lox_callable import LoxCallable
#Method to bind and execute functions

class LoxFunction(LoxCallable):

    def __init__(self, declaration, closure):
        self.declaration = declaration
        self.closure = closure

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        from environment import Environment
        from return_exception import Return

        environment = Environment(self.closure)

        for i in range(len(self.declaration.params)):
            environment.define(
                self.declaration.params[i].lexeme,
                arguments[i]
            )

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as return_value:
            return return_value.value

        return None

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"