import sys
from . import singleton
from inspect import signature
from pathlib import Path
from functools import partial

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
            program_args = self.check_progam_switches()
            if program_args is None:  # exclusive switch was found
                return
            func_args = self.check_required_args(func, program_args)
            result = func(*func_args)
            return result

        singleton.func = inner_func
        return inner_func

    def check_progam_switches(self):
        program_switchs = []
        for i, arg in enumerate(sys.argv[1:]):
            if arg[0] != "-":
                break
            program_switchs.append(arg)
        unknown_switches = [x for x in program_switchs if x not in self.options_map]
        func_args = sys.argv[len(program_switchs) + 1 :]
        if unknown_switches:
            print(f"Unknown switch {unknown_switches[0]} !", file=sys.stderr)
            exit(2)
        for arg in program_switchs:
            func = self.options_map[arg]
            result = func()
            if result is None:  # Exclusive switches return None
                if func_args:
                    print(
                        f"Switch {arg} does not accept extra arguments: {func_args}!",
                        file=sys.stderr,
                    )
                    exit(2)
                return
        return func_args

    def help(self):
        print(f"{self.app_doc}\n")
        print(OPTIONS_HELP)

    def version(self):
        print(f"{self.app_name} {self.app_version}")

    def set_verbosity(self, verbosity):
        singleton.verbosity = verbosity
        return True  # Continue processing arguments

    def check_required_args(self, func, program_args):
        args = []
        i = 1
        sig = signature(func)
        param_str = " ".join([f"<{x}>" for x in sig.parameters])
        for i, param in enumerate(sig.parameters):
            if i >= len(program_args):
                print(
                    f"Missing required command line parameter '{param}' !",
                    file=sys.stderr,
                )
                print(f"Usage:\n  {self.app_name} {param_str}", file=sys.stderr)
                exit(1)
            args.append(program_args[i])
        return args
