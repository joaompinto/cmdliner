# cmdliner

The cmdliber library was inspired on [Cleo](https://github.com/sdispater/cleo).


```python
"""
  A general utility script for testing the cmdliner python library.

  Provides commands that can be used for testing.
"""
from cmdliner import Command, Application


class GreetCommand(Command):
    """
    Greets someone

    greet
        name=John : Who do you want to greet?
        --yell : Yell the name in CAPS ?
        --times=10 : number of times to repeat
    """

    def handle(self, name, yell, times):
        if name:
            text = 'Hello {}'.format(name)
        else:
            text = 'Hello'

        if yell:
            text = text.upper()
        for i in range(times):
            print(text)


app = Application("cmdliner", "0.0", __doc__)
app.add(GreetCommand)
app.run()
```