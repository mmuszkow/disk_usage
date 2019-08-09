#!/usr/bin/env python3

import os
import os.path

# calculates sizes for all directories up to defined depth
def calculate_size(start_dir, depth = 4):
    dir_size = {}

    indexed = 0

    for dir_path, dir_name, file_names in os.walk(start_dir):
        # calculate total size of all files in this directory
        total_size = 0
        for fn in file_names:
            fp = os.path.join(dir_path, fn)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

        # skip empty dirs
        if total_size == 0:
            continue

        # split "/usr/a/b/c" into:
        # /usr
        # /usr/a
        # /usr/a/b
        # /usr/a/b/c
        dirs = dir_path.split(os.sep)[1:depth+1]
        for i in range(1, min(len(dirs) + 1, depth + 1)):
            dir_prefix = os.sep.join(dirs[0:i])
            if not dir_prefix in dir_size:
                dir_size[dir_prefix] = total_size
            else:
                dir_size[dir_prefix] += total_size

        indexed += 1
        if indexed % 10000 == 0:
            print(indexed, 'directories indexed ...')

    return dir_size

# tree node
class Dir:
    def __init__(self, name):
        self.name = name
        self.children = {}
        self.size = 0

    def get(self, name):
        if not name in self.children:
            self.children[name] = Dir(name)
        return self.children[name]

# dictionary to tree
def make_tree(sizes):
    root = Dir('/')
    for dir_name in sizes:
        dirs = dir_name.split(os.sep)
        node = root
        for d in dirs:
            node = node.get(d)
        node.size = sizes[dir_name]
    return root

# dictionary to file
def save_to_file(sizes, fn):
    with open(fn, 'w') as out:
        for key in sorted(sizes, key=sizes.get, reverse=True):
            out.write(key.strip() + '\t' + str(sizes[key]) + '\n')

# dictionary from file
def load_from_file(fn):
    sizes = {}
    with open(fn, 'r') as inp:
        for line in inp:
            try:
                dir_name, size = line.strip().split('\t')
                sizes[dir_name] = int(size)
            except:
                print('Incorrect name', line)
    return sizes

# bytes to proper unit
def int2bytes(val):
    SUFFIX = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    suffix_id = 0
    while val > 1024:
        val /= 1024
        suffix_id += 1
    return '%.2f%s' % (val, SUFFIX[suffix_id])

# pretty print
def print_node(node, min_size = 10 * 1024 * 1024, indent = 0):
    tab = ''
    for i in range(indent): 
        tab += '  '
    print(tab, node.name, int2bytes(node.size))
    for child in sorted(node.children.values(), key=lambda x : x.size, reverse=True):
        if child.size > min_size:
            print_node(child, min_size, indent + 1)

if __name__ == '__main__':
    # load and display old data
    if os.path.isfile('out.txt'):
        root = make_tree(load_from_file('out.txt'))
        print_node(root)

    # calculate, save and display current data
    save_to_file(calculate_size('/'), 'out.txt')
    root = make_tree(load_from_file('out.txt'))
    print_node(root)

