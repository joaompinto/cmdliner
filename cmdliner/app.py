class Application:
    def __init__(self) -> None:
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def run(self):
        print("Running")
