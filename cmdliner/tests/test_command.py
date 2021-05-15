"""
A test utility
"""
import pytest
from unittest.mock import patch

from cmdliner import Command, Application


class Install(Command):
    def handle(self, package_name):
        print(package_name)


def main():
    app = Application()
    app.add_command(Install)
    app.run()


def _test_simple(capsys):
    with patch("sys.argv", ["program_name"]):
        main()
    assert capsys.readouterr().out == "hello\n"


def _test_unsupported_switch(capsys):
    with patch("sys.argv", ["program_name", "--xpto"]):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2


def _test_unsupported_parameter(capsys):
    with patch("sys.argv", ["program_name", "something"]):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 3


def _test_verbose(capsys):
    with patch("sys.argv", ["program_name", "-v"]):
        main()
    assert capsys.readouterr().out == "hello\nPrinted on verbose mode\n"


def _test_very_verbose(capsys):
    with patch("sys.argv", ["program_name", "-vvv"]):
        main()
    assert (
        capsys.readouterr().out == "hello\nPrinted on verbose mode\nVery verbose mode\n"
    )


# if __name__ == "__main__":
#    cli()
