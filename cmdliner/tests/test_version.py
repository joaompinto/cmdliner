import sys
from cmdliner import cli
from pathlib import Path
from unittest.mock import patch


@cli("1.0")
def main():
    print("hello")


def test_version(capsys):
    with patch("sys.argv", ["program_name", "--version"]):
        main()
    assert capsys.readouterr().out == f"{Path(sys.argv[0]).name} 1.0\n"
