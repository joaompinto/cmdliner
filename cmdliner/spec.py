import sys
from collections import namedtuple

CommandSpec = namedtuple(
    # args      list of the required arguments
    # opt_args  list of optional arguments (which provide a default)
    # options   list of options (when they do not provide a default, "False" is the implicit default)
    "Command",
    ["name", "description", "args", "opt_args", "options"],
)


def param2dict(line: str):
    if ":" not in line:
        raise SyntaxError(f"Missing ':' on argument '{line}'")
    name, description = line.split(":")
    name = name.strip()
    description = description.strip()
    return {name: description}


def doc2spec(spec: str) -> CommandSpec:
    cmd_desc = None
    cmd_name = None

    spec_lines = []
    for line in spec.splitlines():
        line = line.strip("\t ")
        if not line:  # skip empty lines
            continue
        if not cmd_desc:  # first the shot description of the command purpose
            cmd_desc = line
        elif not cmd_name:  # second the command name
            cmd_name = line
        elif cmd_name and cmd_desc:  # third the list of arguments
            spec_lines.append(line)

    return CommandSpec(process_arguments(cmd_name, spec_lines))


def process_arguments(cmd_name, spec_lines):
    args = []
    for line in spec_lines:
        try:
            args.append(param2dict(line))
        except SyntaxError:
            print(
                f"Error while parsing command definition for command: {cmd_name}",
                file=sys.stderr,
            )
    raise
