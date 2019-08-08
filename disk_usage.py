#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import os

'''
fig, ax = plt.subplots()

size = 0.3
vals = np.array([[60., 32.], [37., 40.], [29., 10.]])

cmap = plt.get_cmap('tab20c')
outer_colors = cmap(np.arange(3)*4)
inner_colors = cmap(np.array([1, 2, 5, 6, 9, 10]))

ax.pie(vals.sum(axis=1), autopct=lambda pct: func(pct), radius=1, colors=outer_colors,
       wedgeprops=dict(width=size, edgecolor='w'))

ax.pie(vals.flatten(), autopct=lambda pct: func(pct), radius=1-size, colors=inner_colors,
       wedgeprops=dict(width=size, edgecolor='w'))

ax.set(aspect='equal', title='Pie plot with `ax.pie`')
plt.show()
'''


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

def save_to_file(sizes, fn):
    with open(fn, 'w') as out:
        for key in sorted(sizes, key=sizes.get, reverse=True):
            out.write(key.strip() + '\t' + str(sizes[key]) + '\n')

if __name__ == '__main__':
    save_to_file(calculate_size('/'), 'out.txt')

