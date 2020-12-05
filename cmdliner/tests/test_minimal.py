from cmdliner import main, verbose
from unittest.mock import patch


def my_app():
    print("hello")
    verbose(1, "Printed on verbose mode")
    verbose(2, "Printed on very verbose mode")
    verbose(3, "Printed on extra verbose mode")


def minimal_example():
    main("app", "1.0", my_app)


def test_simple(capsys):
    minimal_example()
    assert capsys.readouterr().out == "hello\n"


def test_version(capsys):
    with patch("sys.argv", ["program_name", "--version"]):
        minimal_example()
    assert capsys.readouterr().out == "app 1.0\n"


def test_verbose(capsys):
    with patch("sys.argv", ["program_name", "-v"]):
        minimal_example()
    assert capsys.readouterr().out == "hello\nPrinted on verbose mode\n"
