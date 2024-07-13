import json
import sys
import os
import argparse
from datetime import datetime

def load_structure(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def find_directory(structure, path):
    if path in ('', '.'):
        return structure
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
                return None
        else:
            return None
    return current

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
            return f"{size}{unit}"
        size //= 1024
    return f"{size}P"

def print_ls(directory, show_hidden=False, reverse=False, sort_by_time=False, filter_type=None):
    items = list_directory(directory, show_hidden, filter_type)
    if sort_by_time:
        items.sort(key=lambda x: x['time_modified'])
    if reverse:
        items.reverse()
    for item in items:
        print(item['name'])

def print_ls_long(directory, show_hidden=False, reverse=False, sort_by_time=False, filter_type=None, human_readable=False):
    items = list_directory(directory, show_hidden, filter_type)
    if sort_by_time:
        items.sort(key=lambda x: x['time_modified'])
    if reverse:
        items.reverse()
    for item in items:
        size = human_readable_size(item['size']) if human_readable else item['size']
        time_modified = datetime.fromtimestamp(item['time_modified']).strftime('%b %d %H:%M')
        permissions = item['permissions']
        name = item['name']
        print(f"{permissions} {size} {time_modified} {name}")

def main():
    parser = argparse.ArgumentParser(description='pyls - List directory contents.')
    parser.add_argument('-A', action='store_true', help='do not ignore entries starting with .')
    parser.add_argument('-l', action='store_true', help='use a long listing format')
    parser.add_argument('-r', action='store_true', help='reverse order while sorting')
    parser.add_argument('-t', action='store_true', help='sort by modification time')
    parser.add_argument('-H', action='store_true', help='show human-readable sizes')
    parser.add_argument('--filter', choices=['file', 'dir'], help='filter by type (file or dir)')
    parser.add_argument('path', nargs='?', default='', help='path to list')
    args = parser.parse_args()

    file_path = 'structure.json'
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        sys.exit(1)

    structure = load_structure(file_path)
    directory = find_directory(structure, args.path)
    if directory is None:
        print(f"Error: cannot access '{args.path}': No such file or directory")
        sys.exit(1)

    if args.l:
        print_ls_long(directory, show_hidden=args.A, reverse=args.r, sort_by_time=args.t, filter_type=args.filter, human_readable=args.H)
    else:
        print_ls(directory, show_hidden=args.A, reverse=args.r, sort_by_time=args.t, filter_type=args.filter)

if __name__ == "__main__":
    main()
