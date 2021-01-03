import sys
import argscall.exceptions
from . import singleton
from inspect import signature
from pathlib import Path
from functools import partial
from argscall import argsCaller
from print_err import print_err


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
        self.app_doc = app_doc or "Command does not provide any help text."
        self.app_name = app_name or Path(sys.argv[0]).name

    def __call__(self, func):
        def inner_func():
            self._gather_program_switches()
            self._check_unknown_switches()
            is_exclusive = self._process_program_switches()
            if is_exclusive:
                return None
            return self._process_arguments(func)

        singleton.func = inner_func
        return inner_func

    def _gather_program_switches(self):
        # Consider any leading parameter prefixed with "-" as a program switch
        program_switchs = []
        for i, arg in enumerate(sys.argv[1:]):
            if arg[0] != "-":
                break
            program_switchs.append(arg)
        self.program_switchs = program_switchs

    def _check_unknown_switches(self):
        unknown_switches = [
            x for x in self.program_switchs if x not in self.options_map
        ]
        if unknown_switches:
            print_err(f"Unknown switch {unknown_switches[0]} !", exit_code=2)

    def _process_program_switches(self):
        after_switch_args = sys.argv[len(self.program_switchs) + 1 :]
        for arg in self.program_switchs:
            switch_func = self.options_map[arg]
            exclusive_switch = switch_func()
            if exclusive_switch:
                if after_switch_args:  # exclusive switches do not accept any argumetns
                    print_err(
                        "Switch {arg} does not accept extra arguments: {after_switch_args}!",
                        exit_code=2,
                    )
                return True

    def _process_arguments(self, func):
        after_switch_args = sys.argv[len(self.program_switchs) + 1 :]
        try:
            a_caller = argsCaller(func, *after_switch_args)
        except argscall.exceptions.TooManyArgument as ex:
            print_err(
                f"Got an unexpected argument: (value '{ex.argument_value}')",
                exit_code=3,
            )
        except argscall.exceptions.MissingArgument as ex:
            print_err(f"Missing value for argument {ex.argument_name}", exit_code=3)
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

    def check_required_args(self, func, program_args):
        """
        This function accepts a function, it parses the function signature to determine
        the arguments that at
        eg.

        """
        args = []
        i = 1
        sig = signature(func)
        for p in sig.parameters.values():
            print(p.kind)
        param_str = " ".join([f"<{x}>" for x in sig.parameters])
        print("PP", param_str)
        for i, param in enumerate(sig.parameters):
            if i >= len(program_args):
                print_err(f"Missing required command line parameter '{param}' !")
                print_err(f"Usage:\n  {self.app_name} {param_str}", exit_code=1)
            args.append(program_args[i])
        return args
