#! /usr/local/bin/python3

from datetime import datetime

import os
import sys
import time

HISTORY = []


def update_history(command):
    """
        Updates the history
        @param: command: a list of program and flags
    """
    current_time = datetime.now().strftime("%H:%M")
    str_command = "%s %s" % (current_time, " ".join(command))
    HISTORY.append(str_command)


def new_process(prog, args):
    """
        Fork a new process and execute prog with arg
        @param: prog: a string; the program (or path to program) to execute
        @param: args: a list; the arguments to program
    """
    # fork new process
    proc_id = os.fork()

    # replace memory space with user program
    if proc_id == 0:
        # replace memory space
        os.execlp(prog, prog, *args)
    elif proc_id < 0:
        print("ERROR: Fork failed!")  # Fork failed
    else:
        time.sleep(0.01)


def parse_command(command):
    """
        Parse a command
        @param: command: a list of program and flags
    """
    if len(command) == 0:
        return

    prog, args = command[0], command[1:]
    if prog == "exit":
        print("\n\nThanks for using shlly! Fork our project at https://github.com/marshalhayes/shlly.\n")
        sys.exit(0)
    elif prog == "stat":
        for history in HISTORY:
            print(history)
    elif prog == "cd":
        # chdir sys call to change path
        if args[0] == '-':
            print("Not implemented yet")
        else:
            path = os.path.normpath(args[0])
            os.chdir(path)
    else:
        try:
            new_process(prog, args)
        except FileNotFoundError:
            print("ERROR: Program %s not found" % prog)
            sys.exit(1)


def main():
    pass


if __name__ == "__main__":
    while True:
        try:
            PS1 = "%s ::~> " % os.getcwd()  # prompt
            # collect input and trim trailing whitespace
            command = input(PS1).strip().split('\n')[0].split()
            parse_command(command)
            update_history(command)
        except (KeyboardInterrupt, EOFError):
            # On keyboard interrupt (ctrl-c and EOF (ctrl-d)), exit the program cleanly
            print(
                "\n\nThanks for using shlly! Fork our project at https://github.com/marshalhayes/shlly.\n")
            sys.exit(0)
