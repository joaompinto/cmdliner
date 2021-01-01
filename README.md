# cmdliner

Cmdliner is a python command line parsing library focus on extending scripts/applications with command line parsing features while requiring miminal code for the setup.

## Minimal Use Case
The minimal use case provides `--version` and `-v(vv)` for verbosity:
```python
from cmdliner import cli, verbose

@cli("1.0")
def main():
    print("hello")
    verbose(1, "You see this with -v")

if __name__ == "__main__":
    cli()
```

Testing:
```
$ python test.py
hello
$ python test.py --version
test.py 1.0
$ python test.py -v
hello
You see this with -v
```

## Using command line arguments
```python
from cmdliner import cli


@cli("1.0")
def main(name, age):
    print(f"{name} is {age} years old")


if __name__ == "__main__":
    cli()
```

Result:
```
$ python test.py
Missing required command line parameter 'name' !
Usage:
  test.py <name> <age>
$ python test.py Joe 12
Joe is 12 years old
```

# How to install
```
pip install cmdliner
```
