from cmdliner import singleton
from .application import Application


def main(app_name: str, app_version: str, main_func, test_command=None):
    app = Application(app_name, app_version)
    singleton.app = app
    if app.run():
        main_func()
