"""
:Author: Daniel Mohr
:Email: daniel.mohr@gmx.de
:Date: 2017-02-14
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

from __future__ import print_function
import __future__

from distutils.core import setup, Command

class CheckModules(Command):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@gmx.de
    :Date: 2017-01-08
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

    checking for modules need to run the software
    """
    description = "checking for modules need to run the software"
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import importlib
        summary = ""
        i = 0
        print("checking for modules need to run the software (scripts and")
        print("modules/packages) of this package:\n")
        print("checking for the modules mentioned in the 'setup.py':")
        for module in self.distribution.metadata.get_requires():
            if self.verbose:
                print("try to load %s" % module)
            try:
                importlib.import_module(module)
                if self.verbose:
                    print("  loaded.")
            except ImportError:
                i += 1
                summary += "module '%s' is not available\n" % module
                print("module '%s' is not available <---WARNING---" % module)
        print(
            "\nSummary\n%d modules are not available (not unique)\n%s\n" % (
                i, summary))

class CheckModulesModulefinder(Command):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@gmx.de
    :Date: 2017-01-08
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

    checking for modules need to run the scripts (modulefinder)
    """
    description = "checking for modules need to run the scripts (modulefinder)"
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import modulefinder
        for script in self.distribution.scripts:
            print("\nchecking for modules used in '%s':" % script)
            finder = modulefinder.ModuleFinder()
            finder.run_script(script)
            finder.report()

setup(
    name='pfu',
    version='2017-02-14',
    cmdclass={
        'check_modules': CheckModules,
        'check_modules_modulefinder': CheckModulesModulefinder},
    description='Software to read every file regular (scrubbing).',
    long_description='',
    keywords='scrubbing, silent data corruption',
    author='Daniel Mohr',
    author_email='daniel.mohr@dlr.de',
    maintainer='Daniel Mohr',
    maintainer_email='daniel.mohr@dlr.de',
    url='',
    download_url='',
    packages=[
        'pfu_module',
        'pfu_module.check_checksum',
        'pfu_module.checksum_tools',
        'pfu_module.create_checksum',
        'pfu_module.replicate',
        'pfu_module.replicate.script',
        'pfu_module.replicate.tools',
        'pfu_module.scripts',
        'pfu_module.SimScrub',
        'pfu_module.SimScrub.script',
        'pfu_module.SimScrub.scrubbing',
        'pfu_module.SimScrub.tools'],
    scripts=[
        'scripts/pfu.py'],
    license='GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Operating System :: POSIX :: BSD :: OpenBSD',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'],
    # cat $(find | grep "py$") | egrep -i "^[ \t]*import .*$" | egrep -i --only-matching "import .*$" | sort -u
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
