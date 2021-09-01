"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-05-17, 2021-08-31
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""
import os
import random


def create_random_file(filename):
    with open(filename, 'wb') as fd:
        fd.write(os.urandom(random.randint(23, 42)))


def create_random_directory_tree(
        tmpdir, subdirs=True, number_dirs=None, number_files=None, levels=0):
    # https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap03.html#tag_03_276
    population = bytes(list(range(65, 91))).decode() + \
        bytes(list(range(97, 123))).decode()
    population += bytes(list(range(48, 58))).decode()
    # population += b'._-'.decode()
    population += b'_-'.decode()
    if os.name == 'posix':
        # windows is not able to handle '.' or ' ' at the end of a file name
        # https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file
        population += b'.'.decode()
    my_number_dirs = number_dirs
    if my_number_dirs is None:
        my_number_dirs = random.randint(1, 6)
    my_number_files = number_files
    if my_number_files is None:
        my_number_files = random.randint(2, 6)
    dirs = []
    if levels > 0:
        for i in range(my_number_dirs):
            k = random.randint(6, 23)
            dirname = ''.join(random.choices(population, k=k))
            dirs.append(os.path.join(tmpdir, dirname))
            os.mkdir(dirs[-1])
            if levels > 1:
                create_random_directory_tree(
                    os.path.join(tmpdir, dirs[-1]),
                    subdirs=subdirs,
                    number_dirs=number_dirs,
                    number_files=number_files,
                    levels=levels - 1)
        for i in range(my_number_dirs):
            for j in range(my_number_files):
                k = random.randint(6, 23)
                filename = os.path.join(
                    tmpdir, dirs[i],
                    ''.join(random.choices(population, k=k)))
                create_random_file(filename)
    for j in range(my_number_files):
        k = random.randint(6, 23)
        filename = os.path.join(
            tmpdir,
            ''.join(random.choices(population, k=k)))
        create_random_file(filename)
