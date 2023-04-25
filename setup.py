"""
:Author: Daniel Mohr
:Email: daniel.mohr@gmx.de
:Date: 2023-04-23
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import argparse
import os
import sys

import setuptools


class TestWithPytest(setuptools.Command):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-05-17, 2023-04-20
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

    running automatic tests with pytest
    """
    description = "running automatic tests with pytest"
    user_options = [
        ('src=',
         None,
         'Choose what should be tested; installed: ' +
         'test installed package and scripts (default); ' +
         'local: test package direct from sources ' +
         '(installing is not necessary). ' +
         'The command line scripts are not tested for local. ' +
         'It needs to run with python3. ' +
         'default: installed'),
        ('coverage', None, 'use pytest-cov to generate a coverage report'),
        ('pylint', None, 'if given, run pylint'),
        ('pytestverbose', None, 'increase verbosity of pytest'),
        ('parallel', None, 'run tests in parallel')]

    def initialize_options(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-18
        """
        # pylint: disable=attribute-defined-outside-init
        self.src = 'installed'
        self.coverage = False
        self.pylint = False
        self.pytestverbose = False
        self.parallel = False

    def finalize_options(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04
        """

    def run(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-08-31, 2023-04-20
        """
        # pylint: disable=too-many-branches
        # env python3 setup.py run_pytest
        if self.src == 'installed':
            pass
        elif self.src == 'local':
            sys.path.insert(0, os.path.abspath('src'))
        else:
            raise argparse.ArgumentTypeError(
                "error in command line: " +
                "value for option 'src' is not 'installed' or 'local'")
        sys.path.append(os.path.abspath('.'))
        # https://docs.pytest.org/en/stable/contents.html
        # https://pytest-cov.readthedocs.io/en/latest/
        # pylint: disable=bad-option-value,import-outside-toplevel
        import pytest
        pyargs = []
        if self.parallel:
            try:
                # if available, using parallel test run
                # pylint: disable=unused-variable,unused-import
                import xdist
                if os.name == 'posix':
                    # since we are only running seconds,
                    # we use the load of the last minute:
                    nthreads = int(os.cpu_count() - os.getloadavg()[0])
                    # since we have only a few tests, limit overhead:
                    nthreads = min(4, nthreads)
                    nthreads = max(2, nthreads)  # at least two thread
                else:
                    nthreads = max(2, int(0.5 * os.cpu_count()))
                pyargs += [f'-n {nthreads}']
            except (ModuleNotFoundError, ImportError):
                pass
        if self.coverage:
            # env python3 setup.py run_pytest --coverage
            coverage_dir = 'coverage_report/'
            # first we need to clean the target directory
            if os.path.isdir(coverage_dir):
                files = os.listdir(coverage_dir)
                for filename in files:
                    os.remove(os.path.join(coverage_dir, filename))
            pyargs += ['--cov=pfu_module', '--no-cov-on-fail',
                       '--cov-report=html:' + coverage_dir,
                       '--cov-report=term:skip-covered']
        if self.pylint:
            pyargs += ['--pylint']
        if self.pytestverbose:
            pyargs += ['--verbose']
        pyargs += ['tests/script_pfu_simscrub.py']
        pyargs += ['tests/script_pfu_create_checksum.py']
        pyargs += ['tests/script_pfu_check_checksum.py']
        pyargs += ['tests/script_pfu_replicate.py']
        pyargs += ['tests/script_pfu_speed_test.py']
        if self.src == 'installed':
            pyargs += ['tests/main.py']
        pyplugins = []
        print('call: pytest', ' '.join(pyargs))
        sys.exit(pytest.main(pyargs, pyplugins))


class TestWithUnittest(setuptools.Command):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-05-14, 2023-04-20
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

    running automatic tests with unittest
    """
    description = "running automatic tests with unittest"
    user_options = [
        ("src=",
         None,
         'Choose what should be tested; installed: ' +
         'test installed package and scripts (default); ' +
         'local: test package direct from sources ' +
         '(installing is not necessary). ' +
         'The command line scripts are not tested for local. ' +
         'It needs to run with python3. ' +
         'default: installed')]

    def initialize_options(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04
        """
        # pylint: disable=attribute-defined-outside-init
        self.src = 'installed'

    def finalize_options(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04
        """

    def run(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-08-30, 2023-04-20
        """
        # env python3 setup.py run_unittest
        if self.src == 'installed':
            pass
        elif self.src == 'local':
            sys.path.insert(0, os.path.abspath('src'))
        else:
            raise argparse.ArgumentTypeError(
                "error in command line: " +
                "value for option 'src' is not 'installed' or 'local'")
        sys.path.append(os.path.abspath('.'))
        # pylint: disable=bad-option-value,import-outside-toplevel
        import unittest
        suite = unittest.TestSuite()
        import tests
        setup_self = self

        class TestRequiredModuleImport(unittest.TestCase):
            # pylint: disable=missing-docstring
            # pylint: disable=no-self-use
            def test_required_module_import(self):
                import importlib
                for module in setup_self.distribution.metadata.get_requires():
                    importlib.import_module(module)
        loader = unittest.defaultTestLoader
        suite.addTest(loader.loadTestsFromTestCase(
            TestRequiredModuleImport))
        if self.src == 'installed':
            tests.scripts(suite)
        res = unittest.TextTestRunner(verbosity=2).run(suite)
        if res.wasSuccessful():
            sys.exit(0)
        else:
            sys.exit(1)


class CheckModules(setuptools.Command):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@gmx.de
    :Date: 2017-01-08, 2023-03-31
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

    checking for modules need to run the software
    """
    description = "checking for modules need to run the software"
    user_options = []

    def initialize_options(self):
        """
        :Author: Daniel Mohr
        :Date: 2017-01-08
        """

    def finalize_options(self):
        """
        :Author: Daniel Mohr
        :Date: 2017-01-08
        """

    def run(self):
        """
        :Author: Daniel Mohr
        :Date: 2017-01-08, 2023-03-31, 2023-04-20
        """
        # pylint: disable=bad-option-value,import-outside-toplevel
        import importlib
        summary = ""
        i = 0
        print("checking for modules need to run the software (scripts and")
        print("modules/packages) of this package:\n")
        print("checking for the modules mentioned in the 'setup.py':")
        for module in self.distribution.metadata.get_requires():
            if self.verbose:
                print(f"try to load {module}")
            try:
                importlib.import_module(module)
                if self.verbose:
                    print("  loaded.")
            except ImportError:
                i += 1
                summary += f"module '{module}' is not available\n"
                sys.exit(f"module '{module}' is not available <---WARNING---")
        print(f"\nSummary\n{i} modules are not available (not unique)\n" +
              f"{summary}\n")
        sys.exit(0)


setuptools.setup(
    name='pfu',
    version='2023.04.23',
    cmdclass={
        'check_modules': CheckModules,
        'run_unittest': TestWithUnittest,
        'run_pytest': TestWithPytest},
    description='Software to read every file regular (scrubbing).',
    long_description='',
    keywords='scrubbing, silent data corruption',
    author='Daniel Mohr',
    author_email='daniel.mohr@dlr.de',
    maintainer='Daniel Mohr',
    maintainer_email='daniel.mohr@dlr.de',
    url='https://gitlab.com/dlr-pa/pfu',
    download_url='https://gitlab.com/dlr-pa/pfu',
    package_dir={'': 'src'},
    packages=[
        'pfu_module',
        'pfu_module.check_checksum',
        'pfu_module.checksum_tools',
        'pfu_module.create_checksum',
        'pfu_module.replicate',
        'pfu_module.replicate.script',
        'pfu_module.replicate.tools',
        'pfu_module.scripts',
        'pfu_module.simscrub',
        'pfu_module.simscrub.script',
        'pfu_module.simscrub.scrubbing',
        'pfu_module.simscrub.tools',
        'pfu_module.speed_test',
        'pfu_module.speed_test.script'],
    entry_points={
        'console_scripts':
            ['pfu=pfu_module.scripts.pfu:main'],
    },
    license='GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: '
        'GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Operating System :: POSIX :: BSD :: OpenBSD',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'],
    requires=[
        'argparse',
        'base64',
        'copy',
        'datetime',
        'hashlib',
        'logging',
        'logging.handlers',
        'os',
        'os.path',
        'pickle',
        'platform',
        'random',
        're',
        'signal',
        'subprocess',
        'sys',
        'threading',
        'time'],
    provides=['pfu_module']
)
