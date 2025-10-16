import re

TOKEN_TYPES = {
    'KEYWORD_SET': 'SET',
    'KEYWORD_PRINT': 'PRINT',
    'KEYWORD_IF': 'IF',
    'KEYWORD_THEN': 'THEN',
    'KEYWORD_WHILE': 'WHILE',
    'KEYWORD_END': 'END',
    'IDENTIFIER': 'IDENTIFIER',
    'NUMBER': 'NUMBER',
    'STRING': 'STRING',
    'EQUALS': '=',
    'PLUS': '+',
    'MINUS': '-',
    'MULTIPLY': '*',
    'DIVIDE': '/',
    'COMPARE': 'COMPARE',
    'COMMA': 'COMMA',
    'LINE_BREAK': 'LINE_BREAK',
    'EOF': 'EOF'
}

KEYWORDS = {
    'SET': TOKEN_TYPES['KEYWORD_SET'],
    'PRINT': TOKEN_TYPES['KEYWORD_PRINT'],
    'IF': TOKEN_TYPES['KEYWORD_IF'],
    'THEN': TOKEN_TYPES['KEYWORD_THEN'],
    'WHILE': TOKEN_TYPES['KEYWORD_WHILE'],
    'END': TOKEN_TYPES['KEYWORD_END']
}


class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"


class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.tokenize_all()

    def tokenize_all(self):
        code = re.sub(r'#.*', '', self.code)
        lines = code.strip().split('\n')
        for line in lines:
            if not line.strip():
                continue
            self.tokens.extend(self.tokenize_line(line))
            self.tokens.append(Token(TOKEN_TYPES['LINE_BREAK']))
        self.tokens.append(Token(TOKEN_TYPES['EOF']))

    def tokenize_line(self, line):
        tokens = []
        position = 0
        while position < len(line):
            char = line[position]

            if char.isspace():
                position += 1
                continue

            if char == '"':
                start = position + 1
                end = line.find('"', start)
                if end == -1:
                    raise SyntaxError("Unterminated string literal")
                value = line[start:end]
                tokens.append(Token(TOKEN_TYPES['STRING'], value))
                position = end + 1
                continue

            if char == ',':
                tokens.append(Token(TOKEN_TYPES['COMMA'], ','))
                position += 1
                continue

            if line[position:position+2] in ("==", "!=", "<=", ">="):
                tokens.append(Token(TOKEN_TYPES['COMPARE'], line[position:position+2]))
                position += 2
                continue

            if char in ('<', '>', '=', '+', '-', '*', '/'):
                type_map = {
                    '=': 'EQUALS', '+': 'PLUS', '-': 'MINUS',
                    '*': 'MULTIPLY', '/': 'DIVIDE',
                    '<': 'COMPARE', '>': 'COMPARE'
                }
                tokens.append(Token(TOKEN_TYPES[type_map[char]], char))
                position += 1
                continue

            if char.isdigit():
                start = position
                while position < len(line) and line[position].isdigit():
                    position += 1
                tokens.append(Token(TOKEN_TYPES['NUMBER'], int(line[start:position])))
                continue

            if char.isalpha():
                start = position
                while position < len(line) and (line[position].isalnum() or line[position] == '_'):
                    position += 1
                word = line[start:position].upper()
                token_type = KEYWORDS.get(word, TOKEN_TYPES['IDENTIFIER'])
                tokens.append(Token(token_type, word if token_type == TOKEN_TYPES['IDENTIFIER'] else None))
                continue

            raise SyntaxError(f"Unknown character '{char}' in line: {line}")

        return tokens
