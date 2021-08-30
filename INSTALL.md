# INSTALL: pfu -- Python File Utilities

Version: 2021-05-28

Author: Daniel Mohr

Email: daniel.mohr@dlr.de

## before you install

### Modules

pfu needs the following python modules (most of them are standard and
already in your python installation from a package management)

 * argparse
 * base64
 * hashlib
 * logging
 * logging.handlers
 * os
 * os.path
 * pickle
 * signal
 * sys
 * threading
 * time

and the own modules which comes with this package.

You can also asked the installation routine/script for the python modules:

    python3 setup.py --help
    python3 setup.py --requires

There is also a small extra command to check for availability of
necessary python modules:

    python3 setup.py check_modules

If you want to use this complete software you should have no modules
which are not available.

Much more information you get from the following small extra command
by using the modulefinder:

    python3 setup.py check_modules_modulefinder

It is normal that there are many missing modules reported. Please look
at the details.


### unittests

You can run a few unittests:

    env python3 setup.py run_unittest --src local

But the script is not tested before installing.

After installation you can run unittests on the scripts as well
(see after install).


### pytest

Instead of the standard module unittest you can also use pytest to run
all available unittests (including scripts):

    env python3 setup.py run_pytest

But the scripts are not tested before installing.
After installation you can run these tests on the scripts as well
(see after install).


## install

### global-install

To install this software global to / the following steps are to perform:

    tar xzf pfu-*.tar.*
    cd pfu-*/
    python3 setup.py install


### home-install

To install this software to your $HOME the following steps are to perform:

    tar xzf pfu-*.tar.*
    cd pfu-*/
    python3 setup.py install --home=~


### hints

Keep in mind to have the right pathes.

For the above installation to $HOME the software installs in:

    ~/bin
    ~/lib/python

Please make sure to have these pathes in $PATH and $PYTHONPATH, respectively.
For example:

    export PATH=$PATH:~/bin
    export PYTHONPATH=~/lib/python

If you have installed [argcomplete](https://kislyuk.github.io/argcomplete/)
it is used by pfu and you can use it, e. g. to get bash completion:

    eval "$(register-python-argcomplete3 pfu)"

Similar for other shells, see
[argcomplete](https://kislyuk.github.io/argcomplete/).

## after install

### unittests (after installation)


Now you can run all available unittests (including scripts):

    env python3 setup.py run_unittest


### pytest (after installation)


Instead of the standard module unittest you can also use pytest to run
all available unittests (including scripts):

    env python3 setup.py run_pytest

This command has a few interesting parameters, e. g.:

    env python3 setup.py run_pytest --coverage --parallel
