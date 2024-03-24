if __name__ == "__main__":
    from sys import argv
    from src.interpreter import Interpreter
    match argv:
        case [program, file]:
            with open(file, encoding="utf-8") as f:
                Interpreter.run_script(f.read())
        case [program]:
            Interpreter.run_repl()
