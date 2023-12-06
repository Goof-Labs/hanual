from __future__ import annotations

from template import DocumentationTemplate
from doc_parser import parse_doc_string
from argparse import ArgumentParser
from colorama import init, Fore
from sys import argv
import glob
import ast

init(autoreset=True)


class FunctionVisitor(ast.NodeVisitor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self._documented = []

    @property
    def documented(self):
        return self._documented

    def clear_documented(self):
        self._documented.clear()

    def visit_ClassDef(self, node: ast.ClassDef):
        for method in node.body:
            if not isinstance(method, ast.FunctionDef):
                continue

            doc_string: str | None = ast.get_docstring(method)  # Type: ignore

            if doc_string is None:
                print(f"{Fore.RED}[-]{Fore.RESET} {node.name} >> {method.name}")
                continue

            self._documented.append((node.name, method.name, parse_doc_string(doc_string)))
            print(f"{Fore.GREEN}[+]{Fore.RESET} {node.name} >> {method.name}")

    def visit_FunctionDef(self, node: ast.FunctionDef):
        pass


args = ArgumentParser()
args.add_argument("-p", required=True)
namespace = args.parse_args(argv[1:])

visitor = FunctionVisitor()
dt = DocumentationTemplate()

for file in glob.glob(namespace.p+"\\**\\*.py", recursive=True):
    if "__init__" in file:
        continue

    print(" [ "+file[:-3] + " ]")
    with open(file, "r") as f:
        code = f.read()

    visitor.visit(ast.parse(code))

with open("docs/reference.md", "w") as f:
    f.write(dt.gen_documentation(visitor.documented))
