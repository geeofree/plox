from .scanner import Scanner
from .parser import AstPrinter, Parser

class Interpreter:
    @staticmethod
    def run_script(source):
        tokens = Scanner(source).scan()
        expr = Parser(tokens).parse()
        AstPrinter.print(expr)


    @staticmethod
    def run_repl():
        print("REPL not yet implemented.")
