# main.py

from lexer import Lexer
from parser import Parser

def main():
    input_text = input("Enter the input: ")
    lexer = Lexer(input_text)
    try:
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        result = parser.parse()
        print(result)
    except ValueError as e:
        print(f"Syntax is not correct: {e}")

if __name__ == "__main__":
    main()
