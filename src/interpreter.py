from .scanner import Scanner

class Interpreter:

    @staticmethod
    def run_script(source):
        for token in Scanner(source).scan():
            print(token)


    @staticmethod
    def run_repl():
        print("REPL not yet implemented.")
