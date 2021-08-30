"""
:Author: Daniel Mohr
:Email: daniel.mohr@gmx.de
:Date: 2017-01-08 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import signal
import time
import sys


class MySignalHandler(object):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@gmx.de
    :Date: 2017-01-06 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
    """

    def __init__(self, fcts_to_call):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@gmx.de
        :Date: 2017-01-06 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
        """
        self._fcts_to_call = fcts_to_call
        self._orig_alarm_hndlr = None

    def init(self):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@gmx.de
        :Date: 2017-01-06 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
        """
        signal.signal(signal.SIGINT, self.handler)
        signal.signal(signal.SIGTERM, self.handler)

    def handler(self, signum, _):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@gmx.de
        :Date: 2017-01-06 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
        """
        for fct in self._fcts_to_call:
            fct()
        time.sleep(0.1)
        sys.stderr.write('got signal: %i\n' % signum)
        sys.exit(0)

    def set_alarm(self, count_down_time):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@gmx.de
        :Date: 2017-01-06 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
        """
        if count_down_time > 0:
            self._orig_alarm_hndlr = signal.signal(
                signal.SIGALRM, self.handler)
            signal.alarm(count_down_time)

    def stop_alarm(self):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@gmx.de
        :Date: 2017-01-06 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
        """
        signal.alarm(0)
        if self._orig_alarm_hndlr is not None:
            signal.signal(signal.SIGALRM, self._orig_alarm_hndlr)
