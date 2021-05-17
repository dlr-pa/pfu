"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-05-14
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the script 'pfu.py simscrub'

You can run this file directly::

  env python3 script_pfu_simscrub.py

  pytest-3 script_pfu_simscrub.py

Or you can run only one test, e. g.::

  env python3 script_pfu_simscrub.py script_pfu_simscrub.test_script_pfu_simscrub_help

  pytest-3 -k test_script_pfu_simscrub_help script_pfu_simscrub.py
"""

import os.path
import random
import subprocess
import tempfile
import unittest


def create_random_file(filename):
    with open(filename, 'wb') as fd:
        fd.write(os.urandom(random.randint(23, 42)))


class script_pfu_simscrub(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2021-05-14
    """

    def test_script_pfu_simscrub_help(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-05-14
        """
        cp = subprocess.run(
            ['pfu.py simscrub -h'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True,
            timeout=3, check=True)
        # check begin of help output
        self.assertTrue(cp.stdout.startswith(
            b'usage: pfu.py simscrub '))

    def test_script_pfu_simscrub_0(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-05-14
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            # init scrubbing
            param = '-dir .'
            param += ' -config_data_directory ' + tmpdir
            cp = subprocess.run(
                ['pfu.py simscrub ' + param],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True,
                timeout=3, check=True)
            self.assertEqual(cp.stdout, b'create_directory_trees\n')
            param = '-config_data_directory ' + tmpdir
            #param += ' -fileloglevel 1'
            cp = subprocess.run(
                ['pfu.py simscrub ' + param],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True,
                timeout=3, check=True)
            self.assertEqual(cp.stdout, b'do_scrubbing\n')

    def test_script_pfu_simscrub_1(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-05-14
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            conf_dir = os.path.join(tmpdir, 'conf')
            data_dir = os.path.join(tmpdir, 'data')
            os.mkdir(data_dir)
            for i in range(10):
                create_random_file(os.path.join(data_dir, str(i)))
            # init scrubbing
            param = '-dir ' + data_dir
            param += ' -config_data_directory ' + conf_dir
            cp = subprocess.run(
                ['pfu.py simscrub ' + param],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True,
                timeout=3, check=True)
            self.assertEqual(cp.stdout, b'create_directory_trees\n')
            start_point = os.listdir(conf_dir)[0]
            with open(os.path.join(conf_dir, start_point, 'status')) as fd:
                data = fd.readlines()
            self.assertEqual(data[0], 'I0\n')
            param = '-config_data_directory ' + conf_dir
            param += ' -fileloglevel 1'
            cp = subprocess.run(
                ['pfu.py simscrub ' + param],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True,
                timeout=3, check=True)
            self.assertEqual(cp.stdout, b'do_scrubbing\n')
            with open(os.path.join(conf_dir, start_point, 'log')) as fd:
                data = fd.readlines()
            self.assertTrue(data[-1].endswith(
                'INFO finished scrubbing at 0/10\n'))
            with open(os.path.join(conf_dir, start_point, 'status')) as fd:
                data = fd.readlines()
            self.assertEqual(data[-1], '.')


if __name__ == '__main__':
    unittest.main(verbosity=2)