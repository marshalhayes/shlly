from __future__ import print_function
from datetime import datetime

import os
import sys

HISTORY = []
PREV_DIR = None


def main():
    pass


def update_history(command):
    """
        Updates the history
        :param: command: a list of program and flags
    """
    if command:
        current_time = datetime.now().strftime("%H:%M")
        str_command = "%s %s" % (current_time, command)
        HISTORY.append(str_command)


def new_process(prog, args):
    """
        Fork a new process and execute prog with arg
        :param: str prog: the program (or path to program) to execute
        :param: list args: the arguments to program
    """
    # fork new process
    proc_id = os.fork()

    # replace memory space with user program
    if proc_id == 0:
        # replace memory space
        os.execlp(prog, prog, *args)
        os._exit(0)
    elif proc_id < 0:
        print("ERROR: Fork failed!")  # Fork failed
    else:
        # wait for the child process to complete
        os.waitpid(proc_id, 0)


def parse_command(command):
    """
        Parse a command
        :param: str command: the input program and flags
    """
    global PREV_DIR
    if len(command) == 0:
        return

    command = command.split('\n')[0].split()
    pipe = None  # set to the pipe str (<, >, or |) if a pipe is used

    # if the command contains a pipe, we should handle this differently
    if '<' in command:
        pipe = '<'
    elif '|' in command:
        pipe = '|'
    elif '>' in command:
        pipe = '>'

    if pipe:
        pipe_index = command.index(pipe)  # get the index of the pipe
        prog, args = command[0], command[1:pipe_index]
        prog2, args2 = command[pipe_index+1], command[pipe_index+2:]
        return new_pipe_process(prog, args, prog2, args2, pipe=pipe)

    prog, args = command[0], command[1:]
    if prog == "exit":
        print(
            "\n\nThanks for using shlly! Fork our project at https://github.com/marshalhayes/shlly.\n")
        sys.exit(0)
    elif prog == "stat":
        for history in HISTORY:
            print(history)
    elif prog == "cd":
        if args:
            # chdir sys call to change path
            if args[0] == '-':
                args[0] = PREV_DIR or os.getcwd()
            elif args[0][0] == '~':
                # if the user uses ~ to specify home directory, find the
                # home directory from the environment variable $HOME
                args[0] = args[0].replace('~', os.environ["HOME"])
        # if no path is given as an argument to cd, change directory to $HOME
        path = os.path.normpath(
            args[0] if args else os.environ["HOME"])
        try:
            PREV_DIR = os.getcwd()
            os.chdir(path)
        except FileNotFoundError:
            # if the path isn't valid (there is nothing at that location)
            print("ERROR: %s not found" % path)
    else:
        # a program was called
        try:
            new_process(prog, args)
        except FileNotFoundError:
            print("ERROR: %s not found" % prog)


def new_pipe_process(prog, args, prog2, args2, pipe=None):
    """
        Handle piped command input
        :param: progs; a list of programs to execute (in order)
        :param: args; a list of arguments to pass as input to progs
        :param: pipe; a string indicating which pipe was used (<, >, or |)
    """
    r, w = os.pipe()  # read and write file descriptors

    # depending on which pipe was used, the order of program execution may need to be changed
    if pipe == '|':
        # prog args | prog2 args2
        # create two child processes
        proc_id2 = os.fork()
        proc_id = os.fork()

        # output of first program should be piped into the input of the second program
        if proc_id == 0 and not proc_id2 == 0:
            # child 1
            os.close(r)
            os.dup2(w, 1)  # redirect stdout to write end
            os.dup2(w, 2)  # redirect stderr to write end
            os.execlp(prog, prog, *args)  # execute prog
            os.close(w)
            os._exit(0)
        elif proc_id < 0:
            print("ERROR: Fork failed")

        if proc_id2 == 0:
            # child 2
            os.close(w)
            os.dup2(r, 0)  # redirect read end to stdin
            os.execlp(prog2, prog2, *args2)  # execute prog2
            os._exit(0)
        elif proc_id2 < 0:
            print("ERROR: Fork failed")

        # parent
        os.close(r)
        os.close(w)  # close the write end of the pipe

        # wait for both children to finish
        os.waitpid(proc_id2, 0)
        os.waitpid(proc_id, 0)
    elif pipe == '<':
        # prog args < file
        # fork two child processes
        proc_id2 = os.fork()
        proc_id = os.fork()

        if proc_id == 0 and not proc_id2 == 0:
            os.dup2(w, 1)
            try:
                f = os.open(prog2, os.O_RDONLY)
                fd = os.fdopen(f, 'r')
                contents = fd.read()
                os.write(w, contents.encode())
            except FileNotFoundError:
                print("File %s not found" % prog2)
            os._exit(0)
        elif proc_id < 0:
            print("ERROR: Fork failed")

        if proc_id2 == 0:
            os.dup2(r, 0)
            os.execlp(prog, prog, *args)
            os._exit(0)
        elif proc_id2 < 0:
            print("ERROR: Fork failed")

        os.close(w)
        os.waitpid(proc_id2, 0)
        os.waitpid(proc_id, 0)
    elif pipe == '>':
        # prog args > file
        proc_id = os.fork()  # fork a single child
        if proc_id < 0:
            print("ERROR: Fork failed")
        elif proc_id == 0:
            os.dup2(w, 1)
            os.dup2(w, 2)
            os.execlp(prog, prog, *args)
            os.write(w)
            os._exit(0)
        else:
            os.close(w)
            os.waitpid(proc_id, 0)
            rb = os.fdopen(r, 'r')  # open the read end of the pipe
            contents = rb.read()  # read its contents
            with open(prog2, 'w+') as f:
                # write the contents to the file prog2, ignoring args2 completely
                f.write(contents)


if __name__ == "__main__":
    while True:
        try:
            PS1 = "%s ::~> " % os.getcwd()  # prompt

            # collect input and trim trailing whitespace
            command = input(PS1).strip()
            parse_command(command)
            update_history(command)
        except (KeyboardInterrupt, EOFError):
            # On keyboard interrupt (ctrl-c and EOF (ctrl-d)), exit the program cleanly
            print(
                "\n\nThanks for using shlly! Fork our project at https://github.com/marshalhayes/shlly.\n")
            sys.exit(0)
