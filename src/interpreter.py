from src.ast import AstParser
from .scanner import Scanner
from .parser import Parser

class Interpreter:
    @staticmethod
    def run_script(source):
        tokens = Scanner(source).scan()
        expr = Parser(tokens).parse()
        AstParser.print(expr)


    @staticmethod
    def run_repl():
        print("REPL not yet implemented.")
