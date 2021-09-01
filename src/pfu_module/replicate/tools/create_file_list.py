"""
Author: Daniel Mohr.
Date: 2017-02-14 (last change).
License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import os


def create_file_list(dirpath, filenames):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2015-08-03 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
    """
    filenames.sort()
    file_list = ""
    for name in filenames:
        f = os.path.join(dirpath, name)
        file_list += name + " "
    file_list = file_list.strip()
    return file_list
