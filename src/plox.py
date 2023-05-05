from .scanner import Scanner

class Plox:
    @staticmethod
    def run(file):
        with open(file, 'r') as file:
            scanner = Scanner(file.read())
            tokens = scanner.scan_tokens()
            for token in tokens:
                print(token)


    @staticmethod
    def run_prompt():
        print("run repl")
