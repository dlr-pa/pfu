"""
:Author: Daniel Mohr
:Email: daniel.mohr@gmx.de
:Date: 2017-01-08 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import os
import os.path


def create_file_list(directory, log):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@gmx.de
    :Date: 2017-01-06 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
    """
    n_step = 100
    absfilenames = [None] * n_step
    n_absfilenames = n_step
    i = 0
    for (dirpath, _, filenames) in os.walk(directory):
        for filename in filenames:
            absfilename = os.path.abspath(os.path.join(dirpath, filename))
            if os.path.isfile(absfilename):
                if i >= n_absfilenames:
                    absfilenames += [None] * n_step
                    n_absfilenames += n_step
                absfilenames[i] = absfilename
                i += 1
                log.debug("absfilename: %s" % absfilename)
    return absfilenames[0:i]
