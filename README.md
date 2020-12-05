# cmdliner

A minimal use case that adds name/version printing and verbose selection:

```python
from cmdliner import main, verbose

def my_app():
    print("hello")
    verbose(1, "Printed on verbose mode")
    verbose(2, "Printed on very verbose mode")
    verbose(3, "Printed on extra verbose mode")

main("app", "1.0", my_app)
```
