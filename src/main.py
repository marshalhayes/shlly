#! /usr/bin/python3

import os
import sys
import signal

PS1 = "%s :: ~> " % os.getcwd()

def parse_command(command):
    """
        Parse a command

        command: a list of program and flags
    """
    prog = command[0]
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
