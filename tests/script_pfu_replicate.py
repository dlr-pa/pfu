"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-05-17
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the script 'pfu.py replicate'

You can run this file directly::

  env python3 script_pfu_replicate.py

  pytest-3 script_pfu_replicate.py

Or you can run only one test, e. g.::

  env python3 script_pfu_replicate.py script_pfu_replicate.test_script_pfu_replicate_1

  pytest-3 -k test_script_pfu_replicate_1 script_pfu_replicate.py
"""

import os
import re
import subprocess
import tempfile
import unittest

try:
    from .create_random_directory_tree import create_random_directory_tree
    from .checkoutput_check_checksum import checkoutput
except ModuleNotFoundError:
    from .create_random_directory_tree import create_random_directory_tree
    from .checkoutput_check_checksum import checkoutput


class script_pfu_replicate(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2021-05-17
    """

    def test_script_pfu_replicate_1(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-05-17
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            src_dir = os.path.join(tmpdir, 'src')
            dest_dirs = [os.path.join(tmpdir, 'dest1'),
                         os.path.join(tmpdir, 'dest2'),
                         os.path.join(tmpdir, 'dest3')]
            os.mkdir(src_dir)
            # create random data
            create_random_directory_tree(src_dir, levels=3)
            # create destinations
            param = '-source ' + src_dir
            param += ' -destination ' + ' '.join(dest_dirs)
            cp = subprocess.run(
                ['pfu.py replicate ' + param],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True,
                timeout=28, check=True)
            # check checksums
            for dest_dir in dest_dirs:
                param = '-loglevel 20 -ignore_extension log status'
                param += ' -dir ' + dest_dir
                cp = subprocess.run(
                    ['pfu.py check_checksum ' + param],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    shell=True,
                    timeout=3, check=False)
                self.assertTrue(checkoutput(cp.stderr))


if __name__ == '__main__':
    unittest.main(verbosity=2)
