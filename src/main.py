#! /usr/bin/python3

import os
import sys
import signal
import time

PS1 = "%s :: ~> " % os.getcwd()

def new_process(command):
    # fork new process
    proc_id = os.fork()

    # replace memory space with user program
    if proc_id == 0:
        # replace memory space
        os.execlp(command[0], command[0], command[1:])
    elif proc_id < 0:
        print("ERROR: Fork failed!") # Fork failed
    else:
        print(proc_id)
        time.sleep(None)

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
        new_process(command)
        parse_command(command)
