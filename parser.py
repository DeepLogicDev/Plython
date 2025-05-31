# parser.py

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        current_token = self.current_token()
        if current_token and current_token.type == "IF":
            return self.parse_if_else()
        elif current_token and current_token.type == "FOR":
            return self.parse_for_loop()
        elif current_token and current_token.type == "WHILE":
            return self.parse_while_loop()
        elif current_token and current_token.type in ["INT", "FLOAT", "CHAR"]:
            return self.parse_data_type_declaration()
        elif current_token and current_token.type == "IDENTIFIER":
            return self.parse_array_declaration()
        elif current_token and current_token.type == "DEF":
            return self.parse_function_declaration()
        else:
            raise ParserError("Unexpected token or syntax error")

    def current_token(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def eat(self, token_type):
        token = self.current_token()
        if token and token.type == token_type:
            self.position += 1
            return token
        else:
            raise ParserError(f"Expected token {token_type} but found {token}")

    def parse_if_else(self):
        if self.eat("IF"):
            self.eat("LPAREN")
            self.parse_expression()
            self.eat("RPAREN")
            if self.current_token() and self.current_token().type == "COLON":
                self.eat("COLON")
                self.parse_block_or_statement()
            if self.current_token() and self.current_token().type == "ELSE":
                self.eat("ELSE")
                if self.current_token() and self.current_token().type == "COLON":
                    self.eat("COLON")
                    self.parse_block_or_statement()
            return "Correct syntax"

    def parse_for_loop(self):
        if self.eat("FOR"):
            self.eat("LPAREN")
            self.parse_statement()
            self.parse_expression()
            self.eat("SEMICOLON")
            self.parse_statement()
            self.eat("RPAREN")
            if self.current_token() and self.current_token().type == "COLON":
                self.eat("COLON")
                self.parse_block_or_statement()
            return "Correct syntax"

    def parse_while_loop(self):
        if self.eat("WHILE"):
            self.eat("LPAREN")
            self.parse_expression()
            self.eat("RPAREN")
            if self.current_token() and self.current_token().type == "COLON":
                self.eat("COLON")
                self.parse_block_or_statement()
            return "Correct syntax"

    def parse_data_type_declaration(self):
        token = self.current_token()
        if token.type in ["INT", "FLOAT", "CHAR"]:
            self.eat(token.type)
            self.eat("IDENTIFIER")
            if self.current_token() and self.current_token().type == "ASSIGN":
                self.eat("ASSIGN")
                self.parse_expression()
            if self.current_token() and self.current_token().type == "SEMICOLON":
                self.eat("SEMICOLON")
            return f"{token.value} declaration parsed successfully"
        raise ParserError("Expected a valid data type declaration")

    def parse_array_declaration(self):
        token = self.eat("INT")
        self.eat("IDENTIFIER")
        self.eat("LBRACKET")
        self.eat("LITERAL")
        self.eat("RBRACKET")
        print("Array declaration parsed successfully")
        return f"Array of type {token.value} declared."

    def parse_function_declaration(self):
        self.eat("DEF")
        self.eat("IDENTIFIER")
        self.eat("LPAREN")
        if self.current_token() and self.current_token().type == "RPAREN":
            self.eat("RPAREN")
            self.eat("COLON")
            return "Function declaration parsed successfully"
        else:
            raise ParserError("Expected closing parenthesis for function declaration")

    def parse_expression(self):
        # Parse the left-hand side of the expression
        self.parse_term()
        
        # Check for comparison operators and parse the right-hand side
        while self.current_token() and self.current_token().type in ("EQ", "NEQ", "GREATER", "LESS", "GEQ", "LEQ"):
            operator = self.eat(self.current_token().type)
            self.parse_term()


    def parse_block_or_statement(self):
        if self.current_token() and self.current_token().type == "LCURLY":
            self.eat("LCURLY")
            while self.current_token() and self.current_token().type != "RCURLY":
                self.parse_statement()
            self.eat("RCURLY")
        else:
            self.parse_statement()

    def parse_statement(self):
        if self.current_token() is None:
            raise ParserError("Unexpected end of input; expected a statement")
        if self.current_token().type == "IDENTIFIER":
            self.eat("IDENTIFIER")
            self.eat("ASSIGN")
            if self.current_token().type in ("LITERAL", "IDENTIFIER"):
                self.eat(self.current_token().type)
            else:
                raise ParserError("Expected a literal or identifier in assignment")
        else:
            raise ParserError("Expected an assignment statement")
        
    def parse_term(self):
        token = self.current_token()
        
        if token is None:
            raise ParserError("Unexpected end of input in expression")

        if token.type == "LPAREN":  # Handle nested expressions within parentheses
            self.eat("LPAREN")
            self.parse_expression()
            self.eat("RPAREN")
        elif token.type in ("IDENTIFIER", "LITERAL", "BOOLEAN"):  # Handle literals, identifiers, and booleans
            self.eat(token.type)
        else:
            raise ParserError("Expected an identifier, literal, boolean, or expression in parentheses")

