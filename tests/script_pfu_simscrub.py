"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-05-25, 2021-08-31
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the script 'pfu simscrub'

You can run this file directly::

  env python3 script_pfu_simscrub.py

  pytest-3 script_pfu_simscrub.py

Or you can run only one test, e. g.::

  env python3 script_pfu_simscrub.py script_pfu_simscrub.test_script_pfu_simscrub_0

  pytest-3 -k test_script_pfu_simscrub_help script_pfu_simscrub.py
"""

import os
import random
import subprocess
import tempfile
import unittest

try:
    from .create_random_directory_tree import create_random_file
    from .create_random_directory_tree import create_random_directory_tree
except (ModuleNotFoundError, ImportError):
    from create_random_directory_tree import create_random_file
    from create_random_directory_tree import create_random_directory_tree


class script_pfu_simscrub(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2021-05-25, 2021-08-31
    """

    def test_script_pfu_simscrub_0(self):
        """
        tests 'pfu simscrub'

        :Author: Daniel Mohr
        :Date: 2021-05-25
        """
        cp = subprocess.run(
            'pfu simscrub -h',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True,
            timeout=6, check=True)
        # check begin of help output
        self.assertTrue(cp.stdout.startswith(
            b'usage: pfu simscrub '))

    def test_script_pfu_simscrub_1(self):
        """
        tests 'pfu simscrub'

        :Author: Daniel Mohr
        :Date: 2021-05-25, 2021-08-31
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            # init scrubbing
            param = '-dir .'
            param += ' -config_data_directory ' + tmpdir
            cp = subprocess.run(
                'pfu simscrub ' + param,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True,
                timeout=6, check=True)
            # e. g. on windows we can expect '\r\n' as line ending,
            # on posix systems we can expect '\n' as line ending
            self.assertEqual(cp.stdout,
                             b'create_directory_trees' + os.linesep.encode())
            param = '-config_data_directory ' + tmpdir
            # param += ' -fileloglevel 1'
            cp = subprocess.run(
                'pfu simscrub ' + param,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True,
                timeout=6, check=True)
            self.assertEqual(cp.stdout, b'do_scrubbing' + os.linesep.encode())

    def test_script_pfu_simscrub_2(self):
        """
        tests 'pfu simscrub'

        :Author: Daniel Mohr
        :Date: 2021-05-25, 2021-08-31

        env python3 script_pfu_simscrub.py script_pfu_simscrub.test_script_pfu_simscrub_2
        """
        import pickle
        import stat
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
                'pfu simscrub ' + param,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True,
                timeout=6, check=True)
            # e. g. on windows we can expect '\r\n' as line ending,
            # on posix systems we can expect '\n' as line ending
            self.assertEqual(cp.stdout,
                             b'create_directory_trees' + os.linesep.encode())
            start_point = os.path.join(conf_dir, os.listdir(conf_dir)[0])
            with open(os.path.join(start_point, 'status'), 'rb') as fd:
                data = pickle.load(fd)
            self.assertEqual(data, 0)
            param = '-config_data_directory ' + conf_dir
            param += ' -fileloglevel 1'
            cp = subprocess.run(
                'pfu simscrub ' + param,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True,
                timeout=6, check=True)
            self.assertEqual(cp.stdout, b'do_scrubbing' + os.linesep.encode())
            with open(os.path.join(start_point, 'log')) as fd:
                data = fd.readlines()
            self.assertTrue(data[-1].endswith(
                'INFO finished scrubbing at 0/10\n'))
            with open(os.path.join(start_point, 'status'), 'rb') as fd:
                data = pickle.load(fd)
            self.assertEqual(data, 0)
            # change data
            os.chmod(os.path.join(data_dir, '0'), stat.S_IWRITE)
            create_random_file(os.path.join(data_dir, '1'))
            os.remove(os.path.join(data_dir, '2'))
            create_random_file(os.path.join(data_dir, '10'))
            param += ' -time_delta 0'
            cp = subprocess.run(
                'pfu simscrub ' + param,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True,
                timeout=6, check=True)
            self.assertEqual(cp.stdout, b'do_scrubbing' + os.linesep.encode())

    def test_script_pfu_simscrub_3(self):
        """
        tests 'pfu simscrub'

        :Author: Daniel Mohr
        :Date: 2021-05-25, 2021-08-31
        """
        import pickle
        with tempfile.TemporaryDirectory() as tmpdir:
            conf_dir = os.path.join(tmpdir, 'conf')
            data_dir = os.path.join(tmpdir, 'data')
            os.mkdir(data_dir)
            create_random_directory_tree(data_dir, levels=3)
            # init scrubbing
            param = '-dir ' + data_dir
            param += ' -config_data_directory ' + conf_dir
            cp = subprocess.run(
                'pfu simscrub ' + param,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True,
                timeout=6, check=True)
            # e. g. on windows we can expect '\r\n' as line ending,
            # on posix systems we can expect '\n' as line ending
            self.assertEqual(cp.stdout,
                             b'create_directory_trees' + os.linesep.encode())
            start_point = os.path.join(conf_dir, os.listdir(conf_dir)[0])
            with open(os.path.join(start_point, 'status'), 'rb') as fd:
                data = pickle.load(fd)
            self.assertEqual(data, 0)
            param = '-config_data_directory ' + conf_dir
            param += ' -fileloglevel 1'
            cp = subprocess.run(
                'pfu simscrub ' + param,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True,
                timeout=6, check=True)
            self.assertEqual(cp.stdout, b'do_scrubbing' + os.linesep.encode())
            with open(os.path.join(start_point, 'log')) as fd:
                data = fd.readlines()
            with open(os.path.join(start_point, 'status'), 'rb') as fd:
                data = pickle.load(fd)
            self.assertEqual(data, 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
