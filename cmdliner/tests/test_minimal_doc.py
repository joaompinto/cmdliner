"""
A test utility
"""
from cmdliner import cli
from unittest.mock import patch


@cli("0.0.1", __doc__)
def main():
    pass


HELP_OUTPUT = """
A test utility


OPTIONS:
    --help          : print help
    --version       : print version
    -v, -vv, -vvv   : set verbose level

"""


def test_doc_help(capsys):
    with patch("sys.argv", ["program_name", "--help"]):
        main()
    assert capsys.readouterr().out == HELP_OUTPUT


if __name__ == "__main__":
    cli()
