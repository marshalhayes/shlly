#! /usr/local/bin/python3

from datetime import datetime

import os
import sys

PS1 = "%s :: ~> " % os.getcwd()
COMMANDS = {
    "cd",
    "pwd",
    "stat",
    "exit"
}
HISTORY = []


def update_history(command):
    """
        Updates the history
        @param: command: a list of program and flags
    """
    current_time = datetime.now().strftime("%H:%M")
    str_command = "%s %s" % (current_time, "".join(command))
    HISTORY.append(str_command)


def parse_command(command):
    """
        Parse a command
        @param: command: a list of program and flags
    """
    prog, args = command[0], command[1:]
    if prog == "exit":
        print("\n\nThanks for using shlly! Fork our project at https://github.com/marshalhayes/shlly.\n")
        sys.exit(0)
    elif prog == "stat":
        for history in HISTORY:
            print(history)
    return


def main():
    pass


if __name__ == "__main__":
    while True:
        # collect input and trim trailing whitespace
        command = input(PS1).strip().split('\n')[0].split()
        parse_command(command)
        update_history(command)
