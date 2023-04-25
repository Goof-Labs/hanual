from argparse import ArgumentParser
from sys import exit


parser = ArgumentParser(add_help=True)

parser.add_argument("files", nargs="?")

parser.add_argument(
    "-m",  # mode
    choices=[
        "R",  # Release
        "P",  # Package
        "C",  # compile
        "PD",  # preproc debug
        "LD",  # lexing debug
        "MD",  # Macro debug
        "RD",  # parsing debug
    ],
    default="C",
)

parser.add_argument("-d", nargs="?")

parser.add_argument("-n")

args = parser.parse_args()

if args.files is None:
    parser.print_help()
    print("ERROR: need to include the files you want to compile")
    exit()
