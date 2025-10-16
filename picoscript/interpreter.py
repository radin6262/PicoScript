from .lexer import Lexer, TOKEN_TYPES, Token

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.tokens = []
        self.token_index = 0

    def peek(self):
        return self.tokens[self.token_index] if self.token_index < len(self.tokens) else Token(TOKEN_TYPES['EOF'])

    def consume(self, expected=None):
        token = self.peek()
        if expected and token.type != expected:
            raise RuntimeError(f"Expected {expected}, got {token.type}")
        self.token_index += 1
        return token

    def parse_factor(self):
        token = self.consume()
        if token.type == TOKEN_TYPES['NUMBER']:
            return token.value
        if token.type == TOKEN_TYPES['STRING']:
            return token.value
        if token.type == TOKEN_TYPES['IDENTIFIER']:
            return self.variables.get(token.value, 0)
        raise RuntimeError(f"Unexpected token: {token.type}")

    def parse_term(self):
        result = self.parse_factor()
        while self.peek().type in (TOKEN_TYPES['MULTIPLY'], TOKEN_TYPES['DIVIDE']):
            op = self.consume()
            val = self.parse_factor()
            result = result * val if op.type == TOKEN_TYPES['MULTIPLY'] else int(result / val)
        return result

    def parse_expression(self):
        result = self.parse_term()
        while self.peek().type in (TOKEN_TYPES['PLUS'], TOKEN_TYPES['MINUS']):
            op = self.consume()
            val = self.parse_term()
            result = result + val if op.type == TOKEN_TYPES['PLUS'] else result - val
        return result

    def interpret(self, code):
        self.tokens = Lexer(code).tokens
        self.token_index = 0
        while self.peek().type != TOKEN_TYPES['EOF']:
            self.statement()

    def statement(self):
        while self.peek().type == TOKEN_TYPES['LINE_BREAK']:
            self.consume()
        token = self.peek()
        if token.type == TOKEN_TYPES['KEYWORD_SET']:
            self.consume()
            name = self.consume(TOKEN_TYPES['IDENTIFIER']).value
            self.consume(TOKEN_TYPES['EQUALS'])
            value = self.parse_expression()
            self.variables[name] = value
        elif token.type == TOKEN_TYPES['KEYWORD_PRINT']:
            self.consume()
            outputs = []
            while self.peek().type not in (TOKEN_TYPES['LINE_BREAK'], TOKEN_TYPES['EOF']):
                outputs.append(str(self.parse_expression()))
                if self.peek().type == TOKEN_TYPES['COMMA']:
                    self.consume()
            print(' '.join(outputs))
        else:
            self.consume()
