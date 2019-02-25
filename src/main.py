#! /usr/bin/python

from __future__ import print_function

import os
import sys
import signal

PS1 = "%s :: ~> " % os.getcwd()


def _keyboard_interrupt(signum, frame):
    print("\n\nThanks for using shlly! Fork our project at https://github.com/marshalhayes/shlly.\n")
    sys.exit(0)


def parse_command(command):
    """
        Parse a command

        command: a list of program and flags
    """
    prog = command[0]
    if prog == "exit":
        sys.exit(0)
    return


def main():
    pass


if __name__ == "__main__":
    # exit on keyboard interrupt (ctrl + c)
    signal.signal(signal.SIGINT, _keyboard_interrupt)

    while True:
        # collect input and trim trailing whitespace
        command = raw_input(PS1).strip().split('\n')[0].split()
        parse_command(command)
