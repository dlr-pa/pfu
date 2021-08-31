"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-05-25, 2021-08-31
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the script 'pfu speed_test'

You can run this file directly::

  env python3 script_pfu_speed_test.py

  pytest-3 script_pfu_speed_test.py

Or you can run only one test, e. g.::

  env python3 script_pfu_speed_test.py script_pfu_speed_test.test_script_pfu_speed_test_1

  pytest-3 -k test_script_pfu_speed_test_1 script_pfu_speed_test.py
"""

import os
import re
import subprocess
import tempfile
import unittest


class script_pfu_speed_test(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2021-05-25, 2021-08-31
    """

    def test_script_pfu_speed_test_1(self):
        """
        tests 'pfu speed_test'

        :Author: Daniel Mohr
        :Date: 2021-05-25, 2021-08-31
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            param = '-f a -bytes 42 -count 6 '
            cp = subprocess.run(
                'pfu speed_test ' + param,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir,
                timeout=23, check=True)
            self.assertTrue(
                cp.stderr.endswith(b'finished.' + os.linesep.encode()))

    def test_script_pfu_speed_test_2(self):
        """
        tests 'pfu speed_test'

        :Author: Daniel Mohr
        :Date: 2021-05-25, 2021-08-31
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            param = '-f a -bytes 42 -count 6 -output_format maschine_readable'
            cp = subprocess.run(
                'pfu speed_test ' + param,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir,
                timeout=23, check=True)
            self.assertTrue(
                cp.stderr.endswith(b'finished.' + os.linesep.encode()))


if __name__ == '__main__':
    unittest.main(verbosity=2)
