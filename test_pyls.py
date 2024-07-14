import pytest
from .pyls import human_readable_size, load_structure, find_directory_or_file, list_directory, print_ls_long,print_ls


def test_load_structure():
    structure = load_structure('structure.json')
    assert isinstance(structure, dict)

def test_find_directory_or_file():
    structure = {
        "name": "",
        "contents": [
            {
                "name": "testdir",
                "contents": [
                    {
                        "name": "file1.txt",
                        "size": 100,
                        "time_modified": 1609459200,
                        "permissions": "rw-r--r--"
                    }
                ]
            }
        ]
    }
    item, item_type = find_directory_or_file(structure, 'testdir')
    assert item['name'] == 'testdir'
    assert item_type == 'directory'

    item, item_type = find_directory_or_file(structure, 'testdir/file1.txt')
    assert item['name'] == 'file1.txt'
    assert item_type == 'file'

def test_list_directory():
    directory = {
        "name": "testdir",
        "contents": [
            {
                "name": "file1.txt",
                "size": 100,
                "time_modified": 1609459200,
                "permissions": "rw-r--r--"
            },
            {
                "name": ".hiddenfile",
                "size": 50,
                "time_modified": 1609459200,
                "permissions": "rw-r--r--"
            }
        ]
    }
    items = list_directory(directory, show_hidden=False)
    assert len(items) == 1

    items = list_directory(directory, show_hidden=True)
    assert len(items) == 2

def test_list_directory_filter_file():
    directory = {
        "name": "testdir",
        "contents": [
            {
                "name": "file1.txt",
                "size": 100,
                "time_modified": 1609459200,
                "permissions": "rw-r--r--"
            },
            {
                "name": "subdir",
                "contents": [],
                "time_modified": 1609459200,
                "permissions": "rwxr-xr-x"
            }
        ]
    }
    items = list_directory(directory, filter_type='file')
    assert len(items) == 1
    assert items[0]['name'] == 'file1.txt'

def test_list_directory_filter_dir():
    directory = {
        "name": "testdir",
        "contents": [
            {
                "name": "file1.txt",
                "size": 100,
                "time_modified": 1609459200,
                "permissions": "rw-r--r--"
            },
            {
                "name": "subdir",
                "contents": [],
                "time_modified": 1609459200,
                "permissions": "rwxr-xr-x"
            }
        ]
    }
    items = list_directory(directory, filter_type='dir')
    assert len(items) == 1
    assert items[0]['name'] == 'subdir'

def test_human_readable_size():
    assert human_readable_size(500) == '500'
    assert human_readable_size(1024) == '1.0K'
    assert human_readable_size(1048576) == '1.0M'
    assert human_readable_size(1073741824) == '1.0G'
    assert human_readable_size(1099511627776) == '1.0T'

from io import StringIO
import contextlib

def test_print_ls():
    directory = {
        "name": "testdir",
        "contents": [
            {
                "name": "file1.txt",
                "size": 100,
                "time_modified": 1609459200,
                "permissions": "rw-r--r--"
            },
            {
                "name": "file2.txt",
                "size": 200,
                "time_modified": 1609459200,
                "permissions": "rw-r--r--"
            }
        ]
    }

    output = StringIO()
    with contextlib.redirect_stdout(output):
        print_ls(directory)

    assert "file1.txt" in output.getvalue()
    assert "file2.txt" in output.getvalue()

def test_print_ls_long():
    directory = {
        "name": "testdir",
        "contents": [
            {
                "name": "file1.txt",
                "size": 100,
                "time_modified": 1609459200,
                "permissions": "rw-r--r--"
            },
            {
                "name": "file2.txt",
                "size": 200,
                "time_modified": 1609459200,
                "permissions": "rw-r--r--"
            }
        ]
    }

    output = StringIO()
    with contextlib.redirect_stdout(output):
        print_ls_long(directory)

    assert "file1.txt" in output.getvalue()
    assert "file2.txt" in output.getvalue()
    assert "rw-r--r--" in output.getvalue()