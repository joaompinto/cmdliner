# cmdliner

cmdliner is a python command line parsing library which allows adds command line handling features to your scripts/applications requiring minimal changes to the code.

The minimal use case:
```python
from cmdliner import cli, verbose

# You just need to decorate your "main" function with cli(version)
# version is a required argument, it will be used to provide --version
@cli("1.0")
def main():
    print("hello")
    verbose(1, "You see this with -v")


# Instead of calling your main function directly you call cli(), it will handle
# the argument parsing and invoke the previosly decorated function
if __name__ == "__main__":
    cli()
```

# How to install
```
pip install cmdliner
```
