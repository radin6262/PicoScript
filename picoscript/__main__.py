from .interpreter import Interpreter  # your PicoScript interpreter

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: pico <file.pico>")
        return

    filename = sys.argv[1]
    with open(filename, "r") as f:
        code = f.read()

    interpreter = Interpreter()
    try:
        interpreter.interpret(code)
    except SyntaxError as e:
        print(f"[SYNTAX ERROR] {e}")
    except RuntimeError as e:
        print(f"[RUNTIME ERROR] {e}")
