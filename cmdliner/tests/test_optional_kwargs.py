"""
A test utility
"""
from cmdliner import cli
from unittest.mock import patch


@cli("0.0.1")
def main(**kwargs):
    print(f"Hello {kwargs}")


def test_zero_parameters(capsys):
    with patch("sys.argv", ["program_name"]):
        main()
        assert capsys.readouterr().out == "Hello {}\n"


def test_one_parameter(capsys):
    with patch("sys.argv", ["program_name", "--color=red"]):
        main()
        assert capsys.readouterr().out == "Hello {'color': 'red'}\n"


# def test_two_parameters(capsys):
#     with patch("sys.argv", ["program_name", "abc", "123"]):
#         main()
#         assert capsys.readouterr().out == "Hello abc+123\n"


if __name__ == "__main__":
    cli()
