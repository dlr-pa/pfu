"""
Author: Daniel Mohr.

Date: 2017-02-07 (last change).

License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import logging

def addLoggingLevelName(lvl, levelName):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2016-12-04 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
    """
    methodName = levelName.lower()
    if hasattr(logging, levelName):
        print("debug: levelName already exists")
    if hasattr(logging, methodName):
        print("debug: methodName already exists in logging")
    if hasattr(logging.getLoggerClass(), methodName):
        print("debug: methodName already exists in logging.getLoggerClass")
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(lvl):
            self._log(lvl, message, args, **kwargs)
    def logToRoot(message, *args, **kwargs):
        logging.log(lvl, message, *args, **kwargs)
    logging.addLevelName(lvl, levelName)
    setattr(logging, levelName, lvl)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)

addLoggingLevelName(15, "VERBOSEINFO")

from .read_data_from_file import read_data_from_file

__all__ = ['read_data_from_file']
