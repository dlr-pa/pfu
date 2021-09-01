"""
Author: Daniel Mohr.
Date: 2019-01-09 (last change).
License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import argparse
import logging
import os

from .create_common_parameter import create_common_parameter

__date__ = "2019-01-09"


def speed_test(args):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2017-01-29 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
    """
    log = logging.getLogger("pfu.speed_test")
    import pfu_module.speed_test.script
    pfu_module.speed_test.script.speed_test(args)
    return 0


def create_subparser_speed_test(subparsers):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2019-01-09 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
    """
    myhelp = "You can test the storage read and write speed with this tool.\n"
    myhelp += "To get plausible results, " + \
        "you should write and read more Bytes\n"
    myhelp += "you have as main memory.\n"
    myhelp += "\nBut there are better and faster tools available:\n\n"
    myhelp += " testefestplattengeschwindigkeit.pl\n"
    myhelp += "  https://cadae.de/" + \
        "kleinetools/testefestplattengeschwindigkeit/index.html\n\n"
    myhelp += " fio - flexible I/O tester\n"
    myhelp += "  https://github.com/axboe/fio\n"
    myhelp += "\nExample:\n"
    myhelp += " pfu speed_test -f b -c 2560 -b 4194304"
    epilog = "Author: Daniel Mohr\n"
    epilog += "Date: %s\n" % __date__
    epilog += "License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.\n"
    epilog += "\n%s" % myhelp
    parser = subparsers.add_parser(
        'speed_test',
        description='This script tries to measure the read and write speed ' +
        'of a storage.',
        help='This script tries to measure the read and write speed of a ' +
        'storage.' +
        ' For more help: pfu speed_test -h',
        epilog="%s" % epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.set_defaults(func=speed_test)
    parser.add_argument(
        '-f',
        nargs='+',
        type=str,
        required=True,
        dest='file',
        help='File to use.',
        metavar='f')
    parser.add_argument(
        '-bytes',
        nargs=1,
        type=int,
        required=True,
        dest='bytes',
        help='A block will contain i Bytes.',
        metavar='i')
    parser.add_argument(
        '-count',
        nargs=1,
        type=int,
        required=True,
        dest='count',
        help='Write i times a block.',
        metavar='i')
    parser.add_argument(
        '-output_format',
        nargs=1,
        choices=['human_readable', 'maschine_readable'],
        required=False,
        default=['human_readable'],
        dest='output_format',
        help='Set the output format. default: human_readable ' +
        '(available: human_readable, maschine_readable)',
        metavar='fmt')
    parser.add_argument(
        '-undelete',
        action='store_false',
        default=True,
        required=False,
        dest='delete',
        help='If set, the file will not be deleted afterwards.')
    create_common_parameter(parser)
