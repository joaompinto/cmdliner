import sys
import argscall.exceptions
from pathlib import Path
from functools import partial
from argscall import argsCaller
from print_err import print_err
from . import singleton
from .parser import parse

OPTIONS_HELP = """\
OPTIONS:
    --help          : print help
    --version       : print version
    -v, -vv, -vvv   : set verbose level
"""


class cli(object):
    def __init__(self, app_version=None, app_doc=None, app_name=None):

        self.options_map = {
            "--help": self.help,
            "--version": self.version,
            "-v": partial(self.set_verbosity, 1),
            "-vv": partial(self.set_verbosity, 2),
            "-vvv": partial(self.set_verbosity, 3),
        }

        if app_version is None:
            singleton.func()
        self.app_version = app_version
        self.app_doc = app_doc
        self.app_name = app_name or Path(sys.argv[0]).name

    def __call__(self, func):

        self._set_app_doc(func)

        def inner_func():
            """ This is the core function handling the parsing """
            self._gather_global_switches()
            is_exclusive = self._process_global_switches()
            if is_exclusive:
                return None
            return self._process_arguments(func)

        singleton.func = inner_func
        return inner_func

    def _set_app_doc(self, func):
        if self.app_doc:
            return
        if func.__doc__:
            app_doc = [x[4:] for x in func.__doc__.splitlines()]
            app_doc = "\n".join(app_doc)
        else:
            app_doc = "Command does not provide any help text."
        self.app_doc = app_doc

    def _gather_global_switches(self):
        # Consider any known global switch
        global_switches = []
        for i, arg in enumerate(sys.argv[1:]):
            if arg not in self.options_map:
                break
            global_switches.append(arg)
        self.global_switches = global_switches
        self.args = sys.argv[len(self.global_switches) + 1 :]

    def _process_global_switches(self):
        for arg in self.global_switches:
            switch_func = self.options_map[arg]
            exclusive_switch = switch_func()
            if exclusive_switch:
                if self.args:  # exclusive switches do not accept any argumetns
                    print_err(
                        "Switch {arg} does not accept extra arguments: {self.args}!",
                        exit_code=1,
                    )
                return True

    def _process_arguments(self, func):
        args, kwargs = parse(self.args)
        try:
            a_caller = argsCaller(func, *args, **kwargs)
        except argscall.exceptions.TooManyArgument as ex:
            print_err(
                f"Got an unexpected positional argument: (value '{ex.argument_value}')",
                exit_code=2,
            )
        except argscall.exceptions.MissingArgument as ex:
            print_err(f"Missing value for argument '{ex.argument_name}'", exit_code=3)
        except argscall.exceptions.UnsupportedKeyArgument as ex:
            print_err(f"Missing value for argument '{ex}'", exit_code=4)
        return a_caller.call()

    def help(self):
        print(f"{self.app_doc}\n")
        print(OPTIONS_HELP)
        return True  # is exclusive

    def version(self):
        print(f"{self.app_name} {self.app_version}")
        return True  # is exclusive

    def set_verbosity(self, verbosity):
        singleton.verbosity = verbosity
