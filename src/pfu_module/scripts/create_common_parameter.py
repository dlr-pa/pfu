"""
Author: Daniel Mohr.
Date: 2017-01-29 (last change).
License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import logging


def create_common_parameter(parser):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2017-01-29 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
    """
    # pylint: disable=line-too-long
    parser.add_argument(
        '-logfile',
        nargs=1,
        default=None,
        type=str,
        required=False,
        dest='logfile',
        help='If given, the log output is stored in this file.',
        metavar='i')
    parser.add_argument(
        '-loglevel',
        nargs=1,
        default=[logging.WARNING],
        choices=list(range(1, 51)),
        type=int,
        required=False,
        dest='loglevel',
        help='Set how verbose should be the output to STDOUT. ' +
        'This is the level of logging. Lower numbers give more output. ' +
        'The parameter is a number between 1 and 50. ' +
        'default: %i (logging.WARNING)' % logging.WARNING,
        metavar='i')
    parser.add_argument(
        '-fileloglevel',
        nargs=1,
        default=[logging.INFO],
        choices=list(range(1, 51)),
        type=int,
        required=False,
        dest='logfilelevel',
        help='Set how verbose should be the output to the log file. ' +
        'This is the level of logging. Lower numbers give more output. ' +
        'The parameter is a number between 1 and 50. ' +
        'default: %i (logging.INFO)' % logging.INFO,
        metavar='i')
