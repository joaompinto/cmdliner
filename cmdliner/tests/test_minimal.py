"""
A test utility
"""
import pytest
from cmdliner import cli, verbose
from unittest.mock import patch


@cli("0.0.1")
def main():
    print("hello")
    verbose(1, "Printed on verbose mode")
    verbose(2, "Very verbose mode")


def test_simple(capsys):
    with patch("sys.argv", ["program_name"]):
        main()
    assert capsys.readouterr().out == "hello\n"


def test_unsupported_switch(capsys):
    with patch("sys.argv", ["program_name", "--xpto"]):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2


def test_unsupported_parameter(capsys):
    with patch("sys.argv", ["program_name", "something"]):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 3


def test_verbose(capsys):
    with patch("sys.argv", ["program_name", "-v"]):
        main()
    assert capsys.readouterr().out == "hello\nPrinted on verbose mode\n"


def test_very_verbose(capsys):
    with patch("sys.argv", ["program_name", "-vvv"]):
        main()
    assert (
        capsys.readouterr().out == "hello\nPrinted on verbose mode\nVery verbose mode\n"
    )


if __name__ == "__main__":
    cli()
