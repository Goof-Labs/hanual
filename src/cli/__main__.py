from argparse import ArgumentParser


parser = ArgumentParser(add_help=True)

parser.add_argument("files", nargs="?")

parser.add_argument(
    "--mode",
    choices=[
        "PD",  # parse debug
        "LD",  # lex Debug
        "RD",  # Debug
        "TP",  # Transpile
        "RN",  # release
    ],
    default="TP",
)


args = parser.parse_args()


if not args.files:
    print("No input files")
    parser.exit()
    # stop the program execution


print("goofy")
