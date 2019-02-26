import os
import sys

PS1 = "%s :: ~> " % os.getcwd()
COMMANDS = {
    "cd",
    "pwd",
    "stat",
    "exit"
}
HISTORY = "/tmp/history.txt"


def update_history(command):
    """
        Updates the history file
        @param: command: a list of program and flags
    """
    with open(HISTORY, 'w') as f:
        str_command = "".join(command)
        f.write(str_command)


def parse_command(command):
    """
        Parse a command
        @param: command: a list of program and flags
    """
    prog, args = command[0], command[1:]
    if prog == "exit":
        print("\n\nThanks for using shlly! Fork our project at https://github.com/marshalhayes/shlly.\n")
        sys.exit(0)
    return


def main():
    pass


if __name__ == "__main__":
    while True:
        # collect input and trim trailing whitespace
        command = input(PS1).strip().split('\n')[0].split()
        parse_command(command)
        update_history(command)
