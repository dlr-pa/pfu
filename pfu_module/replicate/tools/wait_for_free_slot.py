"""
Author: Daniel Mohr.
Date: 2017-02-14 (last change).
License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import time

def wait_for_free_slot(processes, number_of_processes, sleeptime):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2015-08-03 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
    """
    free_slot = -1
    while free_slot < 0:
        # check if a slot is free
        for i in range(number_of_processes):
            if processes[i] is None:
                free_slot = i
                break
            elif not (processes[i].poll() is None):
                free_slot = i
                break
        if free_slot < 0:
            time.sleep(sleeptime)
    return free_slot
