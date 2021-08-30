"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-05-25
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the script 'pfu create_checksum'

You can run this file directly::

  env python3 script_pfu_create_checksum.py

  pytest-3 script_pfu_create_checksum.py

Or you can run only one test, e. g.::

  env python3 script_pfu_create_checksum.py script_pfu_create_checksum.test_script_pfu_create_checksum_help

  pytest-3 -k test_script_pfu_create_checksum_help script_pfu_create_checksum.py
"""

import os.path
import random
import subprocess
import tempfile
import unittest


def create_random_file(filename):
    with open(filename, 'wb') as fd:
        fd.write(os.urandom(random.randint(23, 42)))


class script_pfu_create_checksum(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2021-05-25
    """

    def test_script_pfu_create_checksum_help(self):
        """
        tests 'pfu create_checksum'

        :Author: Daniel Mohr
        :Date: 2021-05-25
        """
        cp = subprocess.run(
            'pfu create_checksum -h',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True,
            timeout=6, check=True)
        # check begin of help output
        self.assertTrue(cp.stdout.startswith(
            b'usage: pfu create_checksum '))

    def test_script_pfu_create_checksum_0(self):
        """
        tests 'pfu create_checksum'

        :Author: Daniel Mohr
        :Date: 2021-05-25
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = os.path.join(tmpdir, 'data')
            os.mkdir(data_dir)
            with open(os.path.join(data_dir, 'foo'), 'w') as fd:
                fd.write('bar')
            param = '-dir ' + data_dir
            cp = subprocess.run(
                'pfu create_checksum ' + param,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True,
                timeout=6, check=True)
            with open(os.path.join(data_dir, '.checksum.sha512')) as fd:
                data = fd.readlines()
            self.assertEqual(
                data[0],
                '2CxOtSYcuciqmFXt1n0b0QSC9BUphY2SUJTRc/pmKqkf85vFsYhhUnNIQCHfsW/YKEz2hMzw/Hlb46ovwebBgQ==  foo\n')

    def test_script_pfu_create_checksum_1(self):
        """
        tests 'pfu create_checksum'

        :Author: Daniel Mohr
        :Date: 2021-05-25
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = os.path.join(tmpdir, 'data')
            os.mkdir(data_dir)
            with open(os.path.join(data_dir, 'foo'), 'w') as fd:
                fd.write('bar')
            param = '-dir ' + data_dir
            param += ' -store many'
            cp = subprocess.run(
                'pfu create_checksum ' + param,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True,
                timeout=6, check=True)
            with open(os.path.join(data_dir, 'foo.sha512')) as fd:
                data = fd.readlines()
            self.assertEqual(
                data[0],
                '2CxOtSYcuciqmFXt1n0b0QSC9BUphY2SUJTRc/pmKqkf85vFsYhhUnNIQCHfsW/YKEz2hMzw/Hlb46ovwebBgQ==  foo\n')

    def test_script_pfu_create_checksum_2(self):
        """
        tests 'pfu create_checksum'

        :Author: Daniel Mohr
        :Date: 2021-05-25
        """
        for alg, coding, hashstr in [
                ('md5', 'hex', '37B51D194A7513E45B56F6524F2D51F2  foo\n'),
                ('md5', 'base64', 'N7UdGUp1E+RbVvZSTy1R8g==  foo\n'),
                ('sha256', 'hex', 'FCDE2B2EDBA56BF408601FB721FE9B5C338D10EE429EA04FAE5511B68FBF8FB9  foo\n'),
                ('sha256', 'base64', '/N4rLtula/QIYB+3If6bXDONEO5CnqBPrlURto+/j7k=  foo\n'),
                ('sha512', 'hex', 'D82C4EB5261CB9C8AA9855EDD67D1BD10482F41529858D925094D173FA662AA91FF39BC5B188615273484021DFB16FD8284CF684CCF0FC795BE3AA2FC1E6C181  foo\n'),
                ('sha512', 'base64', '2CxOtSYcuciqmFXt1n0b0QSC9BUphY2SUJTRc/pmKqkf85vFsYhhUnNIQCHfsW/YKEz2hMzw/Hlb46ovwebBgQ==  foo\n')]:
            with tempfile.TemporaryDirectory() as tmpdir:
                data_dir = os.path.join(tmpdir, 'data')
                os.mkdir(data_dir)
                with open(os.path.join(data_dir, 'foo'), 'w') as fd:
                    fd.write('bar')
                param = '-dir ' + data_dir
                param += ' -algorithm ' + alg
                param += ' -coding ' + coding
                cp = subprocess.run(
                    'pfu create_checksum ' + param,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    shell=True,
                    timeout=6, check=True)
                with open(os.path.join(data_dir, '.checksum.' + alg)) as fd:
                    data = fd.readlines()
                self.assertEqual(
                    data[0],
                    hashstr)

    def test_script_pfu_create_checksum_3(self):
        """
        tests 'pfu create_checksum'

        :Author: Daniel Mohr
        :Date: 2021-05-25
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = os.path.join(tmpdir, 'data')
            os.mkdir(data_dir)
            with open(os.path.join(data_dir, 'foo'), 'w') as fd:
                fd.write('bar')
            param = '-dir ' + data_dir
            param += ' -chunk_size 1'
            cp = subprocess.run(
                'pfu create_checksum ' + param,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True,
                timeout=6, check=True)
            with open(os.path.join(data_dir, '.checksum.sha512')) as fd:
                data = fd.readlines()
            self.assertEqual(
                data[0],
                '2CxOtSYcuciqmFXt1n0b0QSC9BUphY2SUJTRc/pmKqkf85vFsYhhUnNIQCHfsW/YKEz2hMzw/Hlb46ovwebBgQ==  foo\n')
            self.assertEqual(
                data[3],
                'qILwrISLC2tMp7Qr+h0mav0N3rqSBK5XqYSmk3bVmBax7z9NRC6opwOWBn/1tw4K6Oqzk1the442bY41w7/hTA==  foo (bytes 2 - 2)\n')


if __name__ == '__main__':
    unittest.main(verbosity=2)
