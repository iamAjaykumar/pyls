# pyls

`pyls` is a simple command-line tool to list directory contents. It provides various options to customize the output, such as long listing format, sorting by modification time, reversing order, and filtering by file type.

## Features

- List directory contents with various formatting options
- Support for hidden files
- Sort by modification time or name
- Reverse sorting order
- Filter by file or directory type
- Display human-readable file sizes

## Installation

### Using `pip`

You can install `pyls` using `pip`:

```sh
pip install .```



### Using `python -m
```sh
python -m pyls```

Usage
The pyls command provides various options to customize the output:

pyls [options] [path]
Options
-A: Do not ignore entries starting with .
-l: Use a long listing format
-r: Reverse order while sorting
-t: Sort by modification time
-h: Show human-readable sizes
--filter: Filter by type (file or dir)
--help: Show help message and exit


Examples
List directory contents in the current directory

pyls
List directory contents in long format

pyls -l
List all files, including hidden ones

pyls -A
List directory contents sorted by modification time

pyls -t
List directory contents in reverse order:

pyls -r
List directory contents with human-readable file sizes

pyls -h
Filter to show only directories:
pyls --filter dir

Filter to show only files
pyls --filter file

Combine multiple options
pyls -l -A -t -r -h --filter file
