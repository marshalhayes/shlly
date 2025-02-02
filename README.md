# shlly

A simple (_and extremely limited_) UNIX shell implemented in Python

Implemented by Marshal Hayes and Xia Fang in COMP 4270 at The University of Memphis.

## Getting Started

- [Running the Shell](#Running-the-Shell)
- [Building from Source](#Building-from-Source)

### Running the Shell

1. Download the binary executable for your system

   - Darwin ([download](https://github.com/marshalhayes/shlly/blob/master/dist/darwin/shlly)):

     ```
     $ curl -O https://raw.github.com/marshalhayes/shlly/dist/darwin/shlly
     ```

   - Linux ([download](https://github.com/marshalhayes/shlly/blob/master/dist/linux/shlly)):

     ```
     $ curl -O https://raw.github.com/marshalhayes/shlly/dist/linux/shlly
     ```

2. Run the executable through the command line. Alternatively, simply double click the file.

   ```
   $ cd <path to the where shlly downloaded>
   $ ./shlly
   ```

   If you receive a permissions-related error message, you may need to add the execute permission to the file. On UNIX-based systems like macOS and Linux, this can be done with the following command.

   ```
   $ sudo chmod +x shlly
   ```

**If you're unable to use the executable, you can just run Shlly with `python`.**

`python src/shlly.py`

### Building from Source

There are many ways to build Python code to executable binaries, but we used the popular `pyinstaller` module to do so. To build from source:

1. Install `pyinstaller`
   ```
   $ pip install pyinstaller
   ```
2. Download the repository
   ```
   $ git clone https://github.com/marshalhayes/shlly
   ```
3. Build the source code to one executable

   ```
   $ cd shlly
   $ pyinstaller --onefile src/shlly.py
   ```

   Two directories `dist` and `build` will be created (if they don't already exist), along with a `.spec` file. The executable exists in the `dist` directory and can only be run on the system architecture it was built on. For example, if the binary was built on macOS, it cannot be executed on Linux or Windows and vice versa.

4. Run the executable

   ```
   $ cd dist
   $ ./shlly
   ```

## What Shlly Supports

- Plain-old programs: Basically any program that you'd execute through a command line interface can be executed through Shlly.
- Pipes: Shlly supports three different pipes (`<`, `|`, and `>`). These pipes can only be used between two programs. For example, `ls -aG | grep Documents` would be valid, but `ls -aG | grep Documents | less` wouldn't be.
- History: We have a basic, custom implementation of `stat` that tracks command history over the current session only. If you close Shlly, the history is destroyed.

## What Shlly Can't Do

- Subshells: `$(...)`
- Multiple commands per line (using `;`): Multiple commands per line seperated with semicolons is not supported. Run each command seperately. Pipes, however, are supported.
- `~` that doesn't refer to `$HOME`: Anywhere that `~` occurs will be replaced with the `$HOME` environment variable. That means that you can't use it for anything else.
- String input: Enter all input without using quotes. If your program or filepath contains spaces, you're out of luck.
- Basically anything else
