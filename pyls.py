#!/usr/bin/env python3
import json
import sys
import os
import argparse
from datetime import datetime

def load_structure(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def find_directory_or_file(structure, path):
    if path in ('', '.'):
        return structure, 'directory'
    parts = path.split('/')
    current = structure
    for part in parts:
        if 'contents' in current:
            found = False
            for item in current['contents']:
                if item['name'] == part:
                    current = item
                    found = True
                    break
            if not found:
                return None, None
        else:
            return None, None
    if 'contents' in current:
        return current, 'directory'
    else:
        return current, 'file'

def list_directory(directory, show_hidden=False, filter_type=None):
    contents = directory.get('contents', [])
    items = [item for item in contents if show_hidden or not item['name'].startswith('.')]
    if filter_type == 'file':
        items = [item for item in items if 'contents' not in item]
    elif filter_type == 'dir':
        items = [item for item in items if 'contents' in item]
    return items

def human_readable_size(size):
    for unit in ['B', 'K', 'M', 'G', 'T']:
        if size < 1024:
            if unit == 'B':
                return f"{size}"
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}P"

def print_ls(directory, show_hidden=False, reverse=False, sort_by_time=False, filter_type=None):
    items = list_directory(directory, show_hidden, filter_type)
    if sort_by_time:
        items.sort(key=lambda x: x['time_modified'], reverse=reverse)
    else:
        items.sort(key=lambda x: x['name'], reverse=reverse)
    if reverse and not sort_by_time:
        items.reverse()
    for item in items:
        print(item['name'],end= "  ")
    print()
    

def print_ls_long(directory, show_hidden=False, reverse=False, sort_by_time=False, filter_type=None, human_readable=False):
    items = list_directory(directory, show_hidden, filter_type)
    if sort_by_time:
        items.sort(key=lambda x: x['time_modified'], reverse=reverse)
    else:
        items.sort(key=lambda x: x['name'])
    if reverse and not sort_by_time:
        items.reverse()
    for item in items:
        size = human_readable_size(item['size']) if human_readable else item['size']
        time_modified = datetime.fromtimestamp(item['time_modified']).strftime('%b %d %H:%M')
        permissions = item['permissions']
        name = item['name']
        print(f"{permissions:<10} {size:>5} {time_modified} {name}")

def print_file_long(file, human_readable=False):
    size = human_readable_size(file['size']) if human_readable else file['size']
    time_modified = datetime.fromtimestamp(file['time_modified']).strftime('%b %d %H:%M')
    permissions = file['permissions']
    name = file['name']
    print(f"{permissions:<10} {size:>5} {time_modified} ./{name}")
def validate_filter(value):
    valid_filters = ['file', 'dir']
    if value not in valid_filters:
        raise argparse.ArgumentTypeError(f"Invalid filter '{value}'. Available filters are 'file' and 'dir'.")
    return value

def main():
    parser = argparse.ArgumentParser(description='pyls - List directory contents.', add_help=False)
    parser.add_argument('-A', action='store_true', help='do not ignore entries starting with .')
    parser.add_argument('-l', action='store_true', help='use a long listing format')
    parser.add_argument('-r', action='store_true', help='reverse order while sorting')
    parser.add_argument('-t', action='store_true', help='sort by modification time')
    parser.add_argument('-h', action='store_true', help='show human-readable sizes')
    parser.add_argument('--filter', type=validate_filter, help='filter by type (file or dir)')
    parser.add_argument('path', nargs='?', default='', help='path to list')
    parser.add_argument('--help', action='help', help='show this help message and exit')
    args = parser.parse_args()

    file_path = 'structure.json'
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        sys.exit(1)

    structure = load_structure(file_path)
    item, item_type = find_directory_or_file(structure, args.path)
    if item is None:
        print(f"Error: cannot access '{args.path}': No such file or directory")
        sys.exit(1)

    if args.l:
        if item_type == 'directory':
            print_ls_long(item, show_hidden=args.A, reverse=args.r, sort_by_time=args.t, filter_type=args.filter, human_readable=args.h)
        elif item_type == 'file':
            print_file_long(item, human_readable=args.h)
    else:
        if item_type == 'directory':
            print_ls(item, show_hidden=args.A, reverse=args.r, sort_by_time=args.t, filter_type=args.filter)
        elif item_type == 'file':
            print(item['name'])

if __name__ == "__main__":
    main()


