from cmdliner import singleton


def verbose(verbosity, message):
    if singleton.app.verbosity >= verbosity:
        print(message)
