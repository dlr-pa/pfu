"""
:Author: Daniel Mohr
:Email: daniel.mohr@gmx.de
:Date: 2017-01-29, 2021-08-31 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import os
import os.path
import random
import threading
import time

import pfu_module.SimScrub.scrubbing
import pfu_module.SimScrub.tools


def do_scrubbing(args, log):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@gmx.de
    :Date: 2017-01-29, 2021-08-31 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
    """
    if os.path.exists(args.config_data_directory[0]):
        start_points = os.listdir(args.config_data_directory[0])
        log.debug("start_points: %s" % start_points)
        # prepare threads
        semaphore_lock = threading.Semaphore(args.number_of_threads[0])
        event_locks = []
        list_of_scrub_inst = []
        list_of_thread_stop_fct = []
        for directory in start_points:
            event_locks += [threading.Event()]
            list_of_scrub_inst += [pfu_module.SimScrub.scrubbing.Scrubbing(
                os.path.join(args.config_data_directory[0],
                             directory),
                semaphore_lock,
                event_locks[-1],
                loglevel=min(args.loglevel[0], args.logfilelevel[0]),
                time_delta=args.time_delta[0],
                chunk_size=args.chunk_size[0],
                reduced_chunk_size=args.reduced_chunk_size[0],
                max_retry=args.max_retry[0],
                omit_chunk_size=args.omit_chunk_size[0],
                update=args.update)]
            list_of_thread_stop_fct += [
                list_of_scrub_inst[-1].stop_scrubbing]
        random.shuffle(list_of_scrub_inst)
        # create signal handling
        my_signal_handling = pfu_module.SimScrub.tools.MySignalHandler(
            list_of_thread_stop_fct)
        my_signal_handling.init()
        my_signal_handling.set_alarm(args.scrub_time[0])
        # start threads
        mythreads = []
        for scrub_inst in list_of_scrub_inst:
            mythreads += [scrub_inst.scrub()]
        # wait for all threads
        for event in event_locks:
            while not event.wait(6):
                pass
        # verify all threads are finished
        for mythread in mythreads:
            #while mythread.isAlive():
            while mythread.is_alive():
                time.sleep(0.1)
