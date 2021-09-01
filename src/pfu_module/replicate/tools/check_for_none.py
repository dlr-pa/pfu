"""
Author: Daniel Mohr.
Date: 2017-02-14 (last change).
License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""


def check_for_none(s):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2015-08-03 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
    """
    ret = 0
    for a in s:
        for b in a:
            if not (b is None):
                ret += 1
    return ret
