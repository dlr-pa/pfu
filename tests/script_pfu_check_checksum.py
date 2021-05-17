"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-05-17
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the script 'pfu.py check_checksum'

You can run this file directly::

  env python3 script_pfu_check_checksum.py

  pytest-3 script_pfu_check_checksum.py

Or you can run only one test, e. g.::

  env python3 script_pfu_check_checksum.py script_pfu_check_checksum.test_script_pfu_check_checksum_1

  pytest-3 -k test_script_pfu_check_checksum_1 script_pfu_check_checksum.py
"""

import os
import random
import re
import subprocess
import tempfile
import unittest


def create_random_file(filename):
    with open(filename, 'wb') as fd:
        fd.write(os.urandom(random.randint(23, 42)))


def create_random_directory_tree(
        tmpdir, subdirs=True, number_dirs=None, number_files=None, levels=0):
    # https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap03.html#tag_03_276
    population = bytes(range(65, 91)).decode() + bytes(range(97, 123)).decode()
    population += bytes(range(48, 58)).decode() + b'._-'.decode()
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


def checkoutput(out):
    out = out.decode()
    ok = True
    regexp_without_hash = re.compile(r'data file without hash: ([0-9]+)')
    regexp_without_data = re.compile(r'hash without data file: ([0-9]+)')
    regexp_matching_hash = re.compile(
        'data file with matching hash\(es\): ([0-9]+)')
    regexp_not_matching_hash = re.compile(
        'data file with not matching hash\(es\): ([0-9]+)')
    for line in out.split('\n'):
        without_hash = regexp_without_hash.findall(line)
        if without_hash and (int(without_hash[0]) != 0):
            ok = False
            break
        without_data = regexp_without_data.findall(line)
        if without_data and (int(without_data[0]) != 0):
            ok = False
            break
        matching_hash = regexp_matching_hash.findall(line)
        if matching_hash and (int(matching_hash[0]) == 0):
            ok = False
            break
        not_matching_hash = regexp_not_matching_hash.findall(line)
        if not_matching_hash and (int(not_matching_hash[0]) != 0):
            ok = False
            break
    return ok


class script_pfu_check_checksum(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2021-05-17
    """

    def test_script_pfu_check_checksum_1(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-05-17
        """
        # run test
        for alg in ['md5', 'sha256', 'sha512']:
            with tempfile.TemporaryDirectory() as tmpdir:
                # create random data
                create_random_directory_tree(tmpdir, levels=3)
                # check error
                param = '-loglevel 20 -dir ' + tmpdir
                cp = subprocess.run(
                    ['pfu.py check_checksum ' + param],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    shell=True,
                    timeout=3, check=True)
                self.assertFalse(checkoutput(cp.stderr))
                # create checksums
                param = '-algorithm ' + alg + ' -dir ' + tmpdir
                cp = subprocess.run(
                    ['pfu.py create_checksum ' + param],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    shell=True,
                    timeout=3, check=True)
                # check checksums
                param = '-loglevel 20 -dir ' + tmpdir
                cp = subprocess.run(
                    ['pfu.py check_checksum ' + param],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    shell=True,
                    timeout=3, check=True)
                self.assertTrue(checkoutput(cp.stderr))

    def test_script_pfu_check_checksum_2(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-05-17
        """
        # check if sha256sum is available
        cp = subprocess.run(
            ['sha256sum --version'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True,
            timeout=3, check=False)
        if cp.returncode != 0:
            self.skipTest('sha256sum not available, skipping test')
            return
        # run test
        with tempfile.TemporaryDirectory() as tmpdir:
            # create random data
            create_random_directory_tree(tmpdir, levels=0)
            # create checksums
            param = '"' + '" "'.join(os.listdir(tmpdir)) + '"'
            cp = subprocess.run(
                ['sha256sum -- ' + param],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir,
                timeout=3, check=True)
            with open(os.path.join(tmpdir, '.checksum'), 'w') as fd:
                fd.write(cp.stdout.decode())
            # check checksums
            param = '-loglevel 20 -dir .'
            cp = subprocess.run(
                ['pfu.py check_checksum ' + param],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir,
                timeout=3, check=True)
            self.assertTrue(checkoutput(cp.stderr))
            param = '-loglevel 20 -dir ' + tmpdir
            cp = subprocess.run(
                ['pfu.py check_checksum ' + param],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True,
                timeout=3, check=True)
            self.assertTrue(checkoutput(cp.stderr))

    def test_script_pfu_check_checksum_3(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-05-17
        """
        # check if sha256sum is available
        cp = subprocess.run(
            ['sha256sum --version'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True,
            timeout=3, check=False)
        if cp.returncode != 0:
            self.skipTest('sha256sum not available, skipping test')
            return
        # run test
        with tempfile.TemporaryDirectory() as tmpdir:
            # create random data
            create_random_directory_tree(tmpdir, levels=0)
            # create checksums
            param = '"' + '" "'.join(os.listdir(tmpdir)) + '"'
            cp = subprocess.run(
                ['sha256sum --tag -- ' + param],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir,
                timeout=3, check=True)
            with open(os.path.join(tmpdir, '.checksum'), 'w') as fd:
                fd.write(cp.stdout.decode())
            # check checksums
            cp = subprocess.run(
                ['pfu.py check_checksum -loglevel 20 -dir .'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir,
                timeout=3, check=True)
            self.assertTrue(checkoutput(cp.stderr))

    def test_script_pfu_check_checksum_4(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-05-17
        """
        # check if sha256 is available
        cp = subprocess.run(
            ['sha256 -s foo'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True,
            timeout=3, check=False)
        if cp.returncode != 0:
            self.skipTest('sha256 not available, skipping test')
            return
        # run test
        with tempfile.TemporaryDirectory() as tmpdir:
            # create random data
            create_random_directory_tree(tmpdir, levels=0)
            # create checksums
            param = '"' + '" "'.join(os.listdir(tmpdir)) + '"'
            cp = subprocess.run(
                ['sha256 -- ' + param],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir,
                timeout=3, check=True)
            with open(os.path.join(tmpdir, '.checksum'), 'w') as fd:
                fd.write(cp.stdout.decode())
            # check checksums
            cp = subprocess.run(
                ['pfu.py check_checksum -loglevel 20 -dir .'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir,
                timeout=3, check=True)
            self.assertTrue(checkoutput(cp.stderr))

    def test_script_pfu_check_checksum_5(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-05-17
        """
        # check if sha256deep is available
        cp = subprocess.run(
            ['sha256deep -V'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True,
            timeout=3, check=False)
        if cp.returncode != 0:
            self.skipTest('sha256deep not available, skipping test')
            return
        # run test
        with tempfile.TemporaryDirectory() as tmpdir:
            # create random data
            create_random_directory_tree(tmpdir, levels=3)
            # create checksums
            cp = subprocess.run(
                ['sha256deep -r -l .'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir,
                timeout=3, check=True)
            with open(os.path.join(tmpdir, '.checksum'), 'w') as fd:
                fd.write(cp.stdout.decode())
            # check checksums
            cp = subprocess.run(
                ['pfu.py check_checksum -loglevel 20 -dir .'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir,
                timeout=3, check=True)
            self.assertTrue(checkoutput(cp.stderr))


if __name__ == '__main__':
    unittest.main(verbosity=2)
