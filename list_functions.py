import ast
from pathlib import Path


def list_functions(filename):
    source = Path(filename).read_text(encoding="utf-8")

    tree = ast.parse(source)

    print(f"\nFunctions in {filename}\n")

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):

            print(f"{node.name}()   Line {node.lineno}")

        elif isinstance(node, ast.AsyncFunctionDef):

            print(f"{node.name}()   Line {node.lineno} (async)")


if __name__ == "__main__":

    filename = input("Python file : ")

    list_functions(filename)