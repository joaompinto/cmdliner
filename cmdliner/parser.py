def parse(input_args):
    """
    Parse a sequence of items which can match one of the following formats:
    --key           # Sets kwargs[key] to True
    --key=value     # Sets kwargs[key] = value
    value           # Sets args

    Returns args, kwargs
    """
    output_args = []
    output_kwargs = {}
    for arg in input_args:
        if arg[0:2] == "--":
            spec = arg[2:]
            if "=" in spec:
                name, value = spec.split("=", 1)
            else:
                name = spec
                value = True
            output_kwargs[name] = value
        else:
            output_args.append(arg)
    return output_args, output_kwargs
