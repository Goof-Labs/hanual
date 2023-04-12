from hanual.lang.pparser import PParser


def make_parse():
    preproc_parser = PParser()

    @preproc_parser.rule("")
    def _():
        ...
