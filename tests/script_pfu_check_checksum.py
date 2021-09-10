"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-05-25
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the script 'pfu check_checksum'

You can run this file directly::

  env python3 script_pfu_check_checksum.py

  pytest-3 script_pfu_check_checksum.py

Or you can run only one test, e. g.::

  env python3 script_pfu_check_checksum.py \
    ScriptPfuCheckChecksum.test_script_pfu_check_checksum_1

  pytest-3 -k test_script_pfu_check_checksum_1 script_pfu_check_checksum.py
"""

import os
import subprocess
import tempfile
import unittest

try:
    from .create_random_directory_tree import create_random_file
    from .create_random_directory_tree import create_random_directory_tree
    from .checkoutput_check_checksum import checkoutput
except (ModuleNotFoundError, ImportError):
    from create_random_directory_tree import create_random_file
    from create_random_directory_tree import create_random_directory_tree
    from checkoutput_check_checksum import checkoutput


class ScriptPfuCheckChecksum(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2021-05-25
    """
    # pylint: disable=invalid-name

    def test_script_pfu_check_checksum_0(self):
        """
        tests 'pfu check_checksum'

        :Author: Daniel Mohr
        :Date: 2021-05-25
        """
        # run test
        with tempfile.TemporaryDirectory() as tmpdir:
            # create random data
            create_random_directory_tree(tmpdir, levels=3)
            # check error
            param = '-loglevel 20 -dir ' + tmpdir
            cpi = subprocess.run(
                'pfu check_checksum ' + param,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True,
                timeout=23, check=True)
            self.assertFalse(checkoutput(cpi.stderr))
            # create checksums
            param = '-dir ' + tmpdir
            subprocess.run(
                'pfu create_checksum ' + param,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True,
                timeout=23, check=False)
            # check checksums
            param = '-loglevel 20 -dir ' + tmpdir
            cpi = subprocess.run(
                'pfu check_checksum ' + param,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True,
                timeout=23, check=True)
            self.assertTrue(checkoutput(cpi.stderr))

    def test_script_pfu_check_checksum_1(self):
        """
        tests 'pfu check_checksum'

        :Author: Daniel Mohr
        :Date: 2021-05-25
        """
        # run test
        for alg in ['md5', 'sha256', 'sha512']:
            for coding in ['hex', 'base16', 'base32', 'base64']:
                for store in ['dir', 'single', 'many']:
                    with tempfile.TemporaryDirectory() as tmpdir:
                        # create random data
                        create_random_directory_tree(tmpdir, levels=3)
                        # create checksums
                        param = '-algorithm ' + alg + ' -dir ' + tmpdir
                        param += ' -coding ' + coding
                        param += ' -store ' + store
                        subprocess.run(
                            'pfu create_checksum ' + param,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            shell=True, cwd=tmpdir,
                            timeout=23, check=False)
                        # check checksums
                        param = '-loglevel 20 -dir ' + tmpdir
                        cpi = subprocess.run(
                            'pfu check_checksum ' + param,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            shell=True, cwd=tmpdir,
                            timeout=23, check=True)
                        self.assertTrue(checkoutput(cpi.stderr))

    def test_script_pfu_check_checksum_2(self):
        """
        tests 'pfu check_checksum'

        :Author: Daniel Mohr
        :Date: 2021-05-25
        """
        # check if sha256sum is available
        cpi = subprocess.run(
            'sha256sum --version',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True,
            timeout=23, check=False)
        if cpi.returncode != 0:
            self.skipTest('sha256sum not available, skipping test')
            return
        # run test
        with tempfile.TemporaryDirectory() as tmpdir:
            # create random data
            create_random_directory_tree(tmpdir, levels=0)
            # create checksums
            param = '"' + '" "'.join(os.listdir(tmpdir)) + '"'
            cpi = subprocess.run(
                'sha256sum -- ' + param,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir,
                timeout=23, check=True)
            with open(os.path.join(tmpdir, '.checksum'), 'w') as fd:
                fd.write(cpi.stdout.decode())
            # check checksums
            param = '-loglevel 20 -dir .'
            cpi = subprocess.run(
                'pfu check_checksum ' + param,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir,
                timeout=23, check=True)
            self.assertTrue(checkoutput(cpi.stderr))
            param = '-loglevel 20 -dir ' + tmpdir
            cpi = subprocess.run(
                'pfu check_checksum ' + param,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True,
                timeout=23, check=True)
            self.assertTrue(checkoutput(cpi.stderr))

    def test_script_pfu_check_checksum_3(self):
        """
        tests 'pfu check_checksum'

        :Author: Daniel Mohr
        :Date: 2021-05-25
        """
        # check if sha256sum is available
        cpi = subprocess.run(
            'sha256sum --version',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True,
            timeout=23, check=False)
        if cpi.returncode != 0:
            self.skipTest('sha256sum not available, skipping test')
            return
        # run test
        with tempfile.TemporaryDirectory() as tmpdir:
            # create random data
            create_random_directory_tree(tmpdir, levels=0)
            # create checksums
            param = '"' + '" "'.join(os.listdir(tmpdir)) + '"'
            cpi = subprocess.run(
                'sha256sum --tag -- ' + param,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir,
                timeout=23, check=True)
            with open(os.path.join(tmpdir, '.checksum'), 'w') as fd:
                fd.write(cpi.stdout.decode())
            # check checksums
            cpi = subprocess.run(
                'pfu check_checksum -loglevel 20 -dir .',
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir,
                timeout=23, check=True)
            self.assertTrue(checkoutput(cpi.stderr))

    def test_script_pfu_check_checksum_4(self):
        """
        tests 'pfu check_checksum'

        :Author: Daniel Mohr
        :Date: 2021-05-25
        """
        # check if sha256 is available
        cpi = subprocess.run(
            'sha256 -s foo',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True,
            timeout=23, check=False)
        if cpi.returncode != 0:
            self.skipTest('sha256 not available, skipping test')
            return
        # run test
        with tempfile.TemporaryDirectory() as tmpdir:
            # create random data
            create_random_directory_tree(tmpdir, levels=0)
            # create checksums
            param = '"' + '" "'.join(os.listdir(tmpdir)) + '"'
            cpi = subprocess.run(
                'sha256 -- ' + param,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir,
                timeout=23, check=True)
            with open(os.path.join(tmpdir, '.checksum'), 'w') as fd:
                fd.write(cpi.stdout.decode())
            # check checksums
            cpi = subprocess.run(
                'pfu check_checksum -loglevel 20 -dir .',
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir,
                timeout=23, check=True)
            self.assertTrue(checkoutput(cpi.stderr))

    def test_script_pfu_check_checksum_5(self):
        """
        tests 'pfu check_checksum'

        :Author: Daniel Mohr
        :Date: 2021-05-25
        """
        # check if sha256deep is available
        cpi = subprocess.run(
            'sha256deep -V',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True,
            timeout=23, check=False)
        if cpi.returncode != 0:
            self.skipTest('sha256deep not available, skipping test')
            return
        # run test
        with tempfile.TemporaryDirectory() as tmpdir:
            # create random data
            create_random_directory_tree(tmpdir, levels=3)
            # create checksums
            cpi = subprocess.run(
                'sha256deep -r -l .',
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir,
                timeout=23, check=True)
            with open(os.path.join(tmpdir, '.checksum'), 'w') as fd:
                fd.write(cpi.stdout.decode())
            # check checksums
            cpi = subprocess.run(
                'pfu check_checksum -loglevel 20 -dir .',
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir,
                timeout=23, check=True)
            self.assertTrue(checkoutput(cpi.stderr))

    def test_script_pfu_check_checksum_6(self):
        """
        tests 'pfu check_checksum' by comparing with sha1sum and sha384sum

        :Author: Daniel Mohr
        :Date: 2021-05-25
        """
        for alg in ['sha1', 'sha384']:
            cmd = alg + 'sum'
            # check if cmd is available
            cpi = subprocess.run(
                cmd + ' --version',
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True,
                timeout=23, check=False)
            if cpi.returncode != 0:
                self.skipTest(cmd + ' not available, skipping test')
                return
            # run test
            with tempfile.TemporaryDirectory() as tmpdir:
                # create random data
                create_random_directory_tree(tmpdir, levels=0)
                # create checksums
                param = '"' + '" "'.join(os.listdir(tmpdir)) + '"'
                cpi = subprocess.run(
                    cmd + ' -- ' + param,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    shell=True, cwd=tmpdir,
                    timeout=23, check=True)
                with open(os.path.join(tmpdir, '.checksum.' + alg), 'w') as fd:
                    fd.write(cpi.stdout.decode())
                # check checksums
                param = '-loglevel 20 -dir .'
                param += ' -hash_extension .' + alg
                cpi = subprocess.run(
                    'pfu check_checksum ' + param,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    shell=True, cwd=tmpdir,
                    timeout=23, check=True)
                self.assertTrue(checkoutput(cpi.stderr))

    def test_script_pfu_check_checksum_7(self):
        """
        tests 'pfu check_checksum' by comparing with sha1 and sha384

        :Author: Daniel Mohr
        :Date: 2021-05-25
        """
        for alg in ['sha1', 'sha384']:
            cmd = alg
            # check if cmd is available
            cpi = subprocess.run(
                cmd + ' -s foo',
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True,
                timeout=23, check=False)
            if cpi.returncode != 0:
                self.skipTest(cmd + ' not available, skipping test')
                return
            # run test
            with tempfile.TemporaryDirectory() as tmpdir:
                # create random data
                create_random_directory_tree(tmpdir, levels=0)
                # create checksums
                param = '"' + '" "'.join(os.listdir(tmpdir)) + '"'
                cpi = subprocess.run(
                    cmd + ' -- ' + param,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    shell=True, cwd=tmpdir,
                    timeout=23, check=True)
                with open(os.path.join(tmpdir, '.checksum.' + alg), 'w') as fd:
                    fd.write(cpi.stdout.decode())
                # check checksums
                param = '-loglevel 20 -dir .'
                param += ' -hash_extension .' + alg
                cpi = subprocess.run(
                    'pfu check_checksum ' + param,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    shell=True, cwd=tmpdir,
                    timeout=23, check=True)
                self.assertTrue(checkoutput(cpi.stderr))

    def test_script_pfu_check_checksum_8(self):
        """
        tests 'pfu check_checksum'

        :Author: Daniel Mohr
        :Date: 2021-05-25
        """
        # run test
        for coding in ['base32', 'base64']:
            for store in ['dir', 'single', 'many']:
                with tempfile.TemporaryDirectory() as tmpdir:
                    # create random data
                    create_random_directory_tree(tmpdir, levels=3)
                    # create checksums
                    param = ' -dir ' + tmpdir
                    param += ' -coding ' + coding
                    param += ' -store ' + store
                    param += ' -chunk_size 23'
                    subprocess.run(
                        'pfu create_checksum ' + param,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        shell=True, cwd=tmpdir,
                        timeout=23, check=False)
                    # check checksums
                    param = '-loglevel 20 -dir ' + tmpdir
                    cpi = subprocess.run(
                        'pfu check_checksum ' + param,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        shell=True, cwd=tmpdir,
                        timeout=23, check=True)
                    self.assertTrue(checkoutput(cpi.stderr))
                    # change data
                    for root, _, files in os.walk(tmpdir):
                        for filename in files:
                            if ((not filename.startswith('.checksum')) and
                                    (not filename.endswith('.sha512'))):
                                create_random_file(
                                    os.path.join(root, filename))
                    # check checksums
                    param = '-loglevel 20 -dir ' + tmpdir
                    cpi = subprocess.run(
                        'pfu check_checksum ' + param,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        shell=True, cwd=tmpdir,
                        timeout=23, check=True)
                    self.assertFalse(checkoutput(cpi.stderr))


if __name__ == '__main__':
    unittest.main(verbosity=2)
