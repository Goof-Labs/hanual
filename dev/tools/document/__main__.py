from __future__ import annotations

import ast
import glob
from argparse import ArgumentParser
from sys import argv

from colorama import Fore
from colorama import init
from doc_parser import parse_doc_string
from template import DocumentationTemplate

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

    def add_file(self, file):
        self._documented.append(file)

    def visit_ClassDef(self, node: ast.ClassDef):
        for method in node.body:
            if not isinstance(method, ast.FunctionDef):
                continue

            doc_string: str | None = ast.get_docstring(method)  # Type: ignore

            if doc_string is None:
                print(f"{Fore.RED}[-]{Fore.RESET} M({node.name}.{method.name})")
                continue

            self._documented.append(
                (node.name, method.name, parse_doc_string(doc_string))
            )
            print(f"{Fore.GREEN}[+]{Fore.RESET} M({node.name}.{method.name})")

    def visit_FunctionDef(self, node: ast.FunctionDef):
        doc_string: str | None = ast.get_docstring(node)  # Type: ignore

        if doc_string is None:
            print(f"{Fore.RED}[-]{Fore.RESET} F({node.name})")
            return

        self._documented.append((node.name, node.name, parse_doc_string(doc_string)))
        print(f"{Fore.GREEN}[+]{Fore.RESET} F({node.name})")


args = ArgumentParser()
args.add_argument("-p", required=True)  # the path to check
args.add_argument("-i", nargs="*", default=[])  # files to ignore

namespace = args.parse_args(argv[1:])

visitor = FunctionVisitor()
dt = DocumentationTemplate()

for file in glob.glob(namespace.p + "\\**\\*.py", recursive=True):
    skip_file = False

    for ignore_case in namespace.i:
        if skip_file:
            continue

        if ignore_case in file:
            skip_file = True

    if skip_file:
        continue

    print(" [ " + file[:-3] + " ]")
    with open(file, "r") as f:
        code = f.read()

    visitor.add_file(file)
    visitor.visit(ast.parse(code))

with open("docs/reference.md", "w") as f:
    f.write(dt.gen_documentation(visitor.documented))
