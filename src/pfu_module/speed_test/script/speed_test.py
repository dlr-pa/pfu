"""
Author: Daniel Mohr.
Date: 2019-01-09, 2021-05-25 (last change).
License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import logging
import os
import random
import re
import time

__date__ = "2019-01-09"

def bytes_to_human_readable(bytes):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2019-01-09 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

    This function converts bytes to a human readable string.
    """
    unit = 'Bytes'
    if bytes >= 1024:
        bytes /= 1024.0
        unit = 'kB'
        if bytes >= 1024:
            bytes /= 1024.0
            unit = 'MB'
            if bytes >= 1024:
                bytes /= 1024.0
                unit = 'GB'
    return '%f %s' % (bytes, unit)

def speed_test(args):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2019-01-09, 2021-05-25 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

    This function tries to measure the read and write speed of a storage.
    """
    args.file[0]
    # logging
    log = logging.getLogger('pfu.speed_test')
    log.setLevel(logging.DEBUG) # logging.DEBUG = 10
    # create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG) # logging.DEBUG = 10
    console_handler.setFormatter(
        logging.Formatter('%(asctime)s %(message)s', datefmt='%H:%M:%S'))
    # add the handlers to log
    log.addHandler(console_handler)
    # print settings and informations
    log.info("pfu speed_test from %s\n" % __date__)
    log.info("setting:")
    log.info(" f: '%s'" % args.file[0])
    log.info(" bytes: %i" % args.bytes[0])
    log.info(" count: %i" % args.count[0])
    log.info(" output_format: '%s'" % args.output_format[0])
    log.info(" delete: %s" % args.delete)
    block = bytes(random.choices(list(range(256)), k=args.bytes[0]))
    if args.output_format[0] == 'human_readable':
        log.info("write %s to '%s'" % (
            bytes_to_human_readable(args.count[0]*args.bytes[0]),
            args.file[0]))
    else:
        log.info("write %i Bytes to '%s'" % (
            args.count[0]*args.bytes[0],
            args.file[0]))
    with open(args.file[0], "wb", 0)as fd:
        t0 = time.perf_counter()
        for i in range(args.count[0]):
            fd.write(block)
        fd.flush()
        os.fsync(fd)
        t1 = time.perf_counter()
    duration = t1-t0
    if args.output_format[0] == 'human_readable':
        log.info(
            'write speed: %s/sec' % bytes_to_human_readable(
                (args.count[0]*args.bytes[0])/duration))
    else:
        log.info('write speed: %f Bytes/sec' % ((args.count[0]*args.bytes[0])/duration))
    if args.output_format[0] == 'human_readable':
        log.info("read %s from '%s'" % (
            bytes_to_human_readable(args.count[0]*args.bytes[0]),
            args.file[0]))
    else:
        log.info("read %i Bytes from '%s'" % (
            args.count[0]*args.bytes[0],
            args.file[0]))
    with open(args.file[0], "rb") as fd:
        t2 = time.perf_counter()
        for i in range(args.count[0]):
            data = fd.read(args.bytes[0])
        t3 = time.perf_counter()
    duration = t3-t2
    if args.output_format[0] == 'human_readable':
        log.info(
            'read speed: %s/sec' % bytes_to_human_readable(
                (args.count[0]*args.bytes[0])/duration))
    else:
        log.info('read speed: %f Bytes/sec' % ((args.count[0]*args.bytes[0])/duration))
    if args.delete:
        os.remove(args.file[0])
        log.info("removed file")
    log.info("finished.")
