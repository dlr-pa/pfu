"""
Author: Daniel Mohr.

Date: 2017-02-07 (last change).

License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import logging

from .read_data_from_file import read_data_from_file


def add_logging_level_name(lvl, levelname):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2016-12-04 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
    """
    methodname = levelname.lower()
    if hasattr(logging, levelname):
        print("debug: levelname already exists")
    if hasattr(logging, methodname):
        print("debug: methodname already exists in logging")
    if hasattr(logging.getLoggerClass(), methodname):
        print("debug: methodname already exists in logging.getLoggerClass")

    def logforlevel(self, message, *args, **kwargs):
        # pylint: disable=missing-docstring,protected-access
        if self.isEnabledFor(lvl):
            self._log(lvl, message, args, **kwargs)

    def logtoroot(message, *args, **kwargs):
        # pylint: disable=missing-docstring
        logging.log(lvl, message, *args, **kwargs)
    logging.addLevelName(lvl, levelname)
    setattr(logging, levelname, lvl)
    setattr(logging.getLoggerClass(), methodname, logforlevel)
    setattr(logging, methodname, logtoroot)


add_logging_level_name(15, "VERBOSEINFO")

__all__ = ['read_data_from_file']
