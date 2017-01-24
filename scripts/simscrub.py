#!/usr/bin/env python2
"""
:Author: Daniel Mohr
:Email: daniel.mohr@gmx.de
:Date: 2017-01-22
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tested on ubuntu 16.04

This script read every file in the given directory tree.
"""

from __future__ import print_function
import __future__

import argparse
import logging
import logging.handlers
import os
import os.path
import sys

import SimScrub.script

__date__ = "2017-01-22"

def main():
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@gmx.de
    :Date: 2017-01-22 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
    """
    myhelp = "You can scrub your data regularly by calling this script via cron or anacron."
    myhelp += "\n\ne. g. in anacron config file (after manually 'simscrub.py -dir bla'):\n"
    myhelp += "  10 15 simscrub_update simscrub.py -time_delta 1 -scrub_time 100 -update\n"
    myhelp += "  1 20 simscrub_scrub simscrub.py -scrub_time 720 -noupdate\n"
    myhelp += ""
    myhelp += ""
    epilog = "Author: Daniel Mohr\n"
    epilog += "Date: %s\n" % __date__
    epilog += "License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.\n"
    epilog += "\n%s" % myhelp
    parser = argparse.ArgumentParser(
        description='This script read every file in the given directory tree.',
        epilog="%s" % epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '-dir',
        nargs='+',
        type=str,
        required=False,
        dest='dir',
        help='Directory tree to scrub.',
        metavar='f')
    cfg_dir = os.path.join(os.path.expanduser("~"), ".simscrub")
    parser.add_argument(
        '-config_data_directory',
        nargs=1,
        default=[cfg_dir],
        type=str,
        required=False,
        dest='config_data_directory',
        help='Set the directory to store configs and data. default: %s' % cfg_dir,
        metavar='n')
    del cfg_dir
    parser.add_argument(
        '-chunk_size',
        nargs=1,
        default=[524288],
        type=int,
        required=False,
        dest='chunk_size',
        help='Set the number of bytes to read at once (reading/scrubbing files). default: 524288',
        metavar='n')
    parser.add_argument(
        '-reduced_chunk_size',
        nargs=1,
        default=[1024],
        type=int,
        required=False,
        dest='reduced_chunk_size',
        help='Set the number of bytes to try to read on error (IOError) at once. default: 1024',
        metavar='n')
    parser.add_argument(
        '-max_retry',
        nargs=1,
        default=[3],
        type=int,
        required=False,
        dest='max_retry',
        help='Set the number of retries on IOError. default: 3',
        metavar='n')
    parser.add_argument(
        '-omit_chunk_size',
        nargs=1,
        default=[1024],
        type=int,
        required=False,
        dest='omit_chunk_size',
        help='Set the number of bytes to omit if an IOERRO occurs. Should be greater or equal reduced_chunk_size. default: 1024',
        metavar='n')
    parser.add_argument(
        '-time_delta',
        nargs=1,
        default=[42],
        type=int,
        required=False,
        dest='time_delta',
        help='Set the number of seconds between status is saved. default: 42',
        metavar='n')
    parser.add_argument(
        '-number_of_threads',
        nargs=1,
        default=[1],
        type=int,
        required=False,
        dest='number_of_threads',
        help='Set the number of threads to use (only one thread per directory tree). default: 1',
        metavar='n')
    parser.add_argument(
        '-scrub_time',
        nargs=1,
        default=[-1],
        type=int,
        required=False,
        dest='scrub_time',
        help='Set the seconds for scrubbing. If set to 0, scrubbing is done until all files are read. Only working on Unix systems. default: 0',
        metavar='n')
    parser.add_argument(
        '-loglevel',
        nargs=1,
        default=[logging.WARNING],
        choices=range(1, 51),
        type=int,
        required=False,
        dest='loglevel',
        help='Set how verbose should be the output to STDOUT. This is the level of logging. Lower numbers give more output. The parameter is a number between 1 and 50. default: %i (logging.WARNING)' % logging.WARNING,
        metavar='i')
    parser.add_argument(
        '-fileloglevel',
        nargs=1,
        default=[logging.INFO],
        choices=range(1, 51),
        type=int,
        required=False,
        dest='logfilelevel',
        help='Set how verbose should be the output to the log file. This is the level of logging. Lower numbers give more output. The parameter is a number between 1 and 50. default: %i (logging.INFO)' % logging.INFO,
        metavar='i')
    parser.add_argument(
        '-update',
        action='store_true',
        required=False,
        dest='update',
        help='If set update each directory tree before scrubbing. (default)')
    parser.add_argument(
        '-noupdate',
        action='store_false',
        required=False,
        dest='update',
        help='If set do not update the directory tree before scrubbing.')
    parser.set_defaults(update=True)
    args = parser.parse_args()
    # create logging
    log = logging.getLogger("simscrub")
    log_console_handler = logging.StreamHandler()
    log_console_handler.setFormatter(
        logging.Formatter('%(asctime)s %(threadName)s %(levelname)s %(message)s',
                          datefmt='%Y-%m-%d %H:%M:%S'))
    log_console_handler.setLevel(args.loglevel[0])
    log.addHandler(log_console_handler)
    log.setLevel(min(args.loglevel[0], args.logfilelevel[0]))
    if args.dir is not None: # create file list
        SimScrub.script.create_directory_trees(args, log)
    else: # search for configs and data
        SimScrub.script.do_scrubbing(args, log)
    sys.exit(0) # success

if __name__ == "__main__":
    main()
