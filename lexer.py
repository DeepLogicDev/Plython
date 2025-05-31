# lexer.py

import re

TOKEN_TYPES = {
    'IF': r'\bif\b',
    'ELSE': r'\belse\b',
    'ELIF': r'\belif\b',
    'FOR': r'\bfor\b',
    'WHILE': r'\bwhile\b',
    'IN': r'\bin\b',
    'DEF': r'\bdef\b',
    'LPAREN': r'\(',
    'RPAREN': r'\)',
    'IDENTIFIER': r'\b[a-zA-Z_][a-zA-Z0-9_]*\b',
    'LITERAL': r'\b[0-9]+\b',
    'BOOLEAN': r'\b(True|False)\b',
    'EQ': r'==',
    'ASSIGN': r'=',
    'NEQ': r'!=',
    'GREATER': r'>',
    'LESS': r'<',
    'GEQ': r'>=',
    'LEQ': r'<=',
    'AND': r'and',
    'OR': r'or',
    'PLUS': r'\+',
    'MINUS': r'-',
    'MULTIPLY': r'\*',
    'DIVIDE': r'/',
    'COLON': r':',
    'NEWLINE': r'\n',
}

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, '{self.value}')"

class Lexer:
    def __init__(self, input_text):
        self.input_text = input_text
        self.tokens = []
        self.position = 0

    def tokenize(self):
        while self.position < len(self.input_text):
            if self.input_text[self.position].isspace():
                if self.input_text[self.position] == '\n':
                    self.tokens.append(Token('NEWLINE', '\n'))
                self.position += 1
                continue

            match = None
            for token_type, pattern in TOKEN_TYPES.items():
                regex = re.compile(pattern)
                match = regex.match(self.input_text, self.position)
                if match:
                    value = match.group(0)
                    self.tokens.append(Token(token_type, value))
                    self.position = match.end()
                    break

            if not match:
                raise ValueError(f"Unexpected character '{self.input_text[self.position]}' at position {self.position}")

        return self.tokens
