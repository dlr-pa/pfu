"""
Author: Daniel Mohr.
Date: 2017-02-14 (last change).
License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import subprocess
import time

from .check_for_none import check_for_none
from .wait_for_free_slot import wait_for_free_slot


def run_check_checksums(args, log, commands_check_checksums,
                        text="", summary=""):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2015-08-03 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
    """
    check_checksums_errors = ""
    runs = dict()
    runs['processes'] = [None] * args.number_of_processes
    runs['cmd'] = [None] * args.number_of_processes
    runs['id0'] = [None] * args.number_of_processes
    runs['id1'] = [None] * args.number_of_processes
    commands_check_checksums_run = [False] * len(commands_check_checksums)
    commands_check_checksums_is_running = []
    for i0 in range(len(commands_check_checksums)):
        commands_check_checksums_is_running += [[]]
        for i1 in range(len(commands_check_checksums[i0])):
            commands_check_checksums_is_running[i0] += [False]
    while check_for_none(commands_check_checksums) > 0:
        i = wait_for_free_slot(
            runs['processes'], args.number_of_processes, args.sleeptime)
        if not (runs['processes'][i] is None):
            stat = "process '%s' terminated with %d" % (
                runs['cmd'][i], runs['processes'][i].returncode)
            log.info(stat)
            summary += stat + "\n"
            if runs['processes'][i].returncode != 0:
                check_checksums_errors += stat + "\n"
            runs['processes'][i] = None
            id0 = runs['id0'][i]
            id1 = runs['id1'][i]
            commands_check_checksums_run[id0] = False
            commands_check_checksums[id0][id1] = None
            commands_check_checksums_is_running[i0][i1] = False
        # find command to run
        id0 = -1
        id1 = -1
        for i0 in range(len(commands_check_checksums)):
            if ((commands_check_checksums_run[i0] is False) or
                    (args.limit_number_of_processes_to_distinations == 0)):
                for i1 in range(len(commands_check_checksums[i0])):
                    if ((not (commands_check_checksums[i0][i1] is None)) and
                            (not commands_check_checksums_is_running[i0][i1])):
                        id0 = i0
                        id1 = i1
                        break
                if id0 >= 0:
                    break
        if (id0 >= 0) and (id1 >= 0):
            # start subprocess
            runs['processes'][i] = subprocess.Popen(
                commands_check_checksums[id0][id1], bufsize=-1, shell=True)
            runs['cmd'][i] = commands_check_checksums[id0][id1]
            runs['id0'][i] = id0
            runs['id1'][i] = id1
            commands_check_checksums_run[id0] = True
            commands_check_checksums_is_running[i0][i1] = True
            log.info("started '%s'" % commands_check_checksums[id0][id1])
        else:
            for i in range(args.number_of_processes):
                if not (runs['processes'][i] is None):
                    if not (runs['processes'][i].poll() is None):
                        stat = "process '%s' terminated with %d" % (
                            runs['cmd'][i], runs['processes'][i].returncode)
                        log.info(stat)
                        summary += stat + "\n"
                        if runs['processes'][i].returncode != 0:
                            check_checksums_errors += stat + "\n"
                        runs['processes'][i] = None
                        id0 = runs['id0'][i]
                        id1 = runs['id1'][i]
                        commands_check_checksums_run[id0] = False
                        commands_check_checksums[id0][id1] = None
                        commands_check_checksums_is_running[i0][i1] = False
            time.sleep(args.sleeptime)
    # wait until all processes are ready
    log.info(text)
    for i in range(args.number_of_processes):
        if not (runs['processes'][i] is None):
            runs['processes'][i].wait()
            stat = "process '%s' terminated with %d" % (
                runs['cmd'][i], runs['processes'][i].returncode)
            log.info(stat)
            summary += stat + "\n"
            if runs['processes'][i].returncode != 0:
                check_checksums_errors += stat + "\n"
            runs['processes'][i] = None
            id0 = runs['id0'][i]
            id1 = runs['id1'][i]
            commands_check_checksums_run[id0] = False
            commands_check_checksums[id0][id1] = None
            commands_check_checksums_is_running[i0][i1] = False
    return summary, check_checksums_errors
