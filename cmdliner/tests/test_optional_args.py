"""
A test utility
"""
from cmdliner import cli

#  from unittest.mock import patch


@cli("0.0.1")
def main(*args):
    print(f"Hello {'+'.join(args)}")


# def test_zero_parameters(capsys):
#     with patch("sys.argv", ["program_name"]):
#         assert capsys.readouterr().out == "Hello \n"


if __name__ == "__main__":
    cli()
