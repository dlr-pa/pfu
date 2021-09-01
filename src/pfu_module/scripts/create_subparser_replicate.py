"""
Author: Daniel Mohr.
Date: 2017-02-14, 2021-05-17 (last change).
License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import argparse

from .create_common_parameter import create_common_parameter

__date__ = "2021-05-17"


def replicate(args):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2017-02-14 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
    """
    import pfu_module.replicate.script
    pfu_module.replicate.script.replicate(args)


def create_subparser_replicate(subparsers):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2017-02-14, 2021-05-17 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

    This is the code for the script :program:`pfu`.
    In this function only the command line parameters for 'replicate'
    are defined.
    """
    myhelp = "Examples:\n\n"
    myhelp += "  time pfu replicate -source sd -destination $(pwd)/t1 t2/\n\n"
    myhelp += "  time pfu replicate -so ./sd -de t1 t2/ -l 0\n\n"
    myhelp += "  time pfu replicate -checksum_check_parameter " + \
        "'--quiet --check' \\\n   -source sd/ -destination t1/ t2/\n\n"
    myhelp += "  time pfu replicate -checksum_program md5sum " + \
        "-source sd -destination t1 t2\n\n"
    myhelp += "  time pfu replicate -copy_program1 cp \\\n   " + \
        "-copy_parameter1 '--recursive --archive --update " + \
        "--one-file-system --no-dereference' \\\n   -source sd " + \
        "-destination t1 t2\n\n"
    myhelp += "It takes a long time, e. g.:\n"
    myhelp += "  >>> data = 1.0 * 1024*1024*1024*1024 # 1.0 [TB]\n"
    myhelp += "  >>> copytime = data / (100*1024*1024) / 60.0 / 60.0 " + \
        "# [h] (at 100 MB/sec)\n"
    myhelp += "  >>> calculatechecksumtime = " + \
        "data/(150*1024*1024)/60.0/60.0 # [h] (at 150 MB/sec with sha256sum)\n"
    myhelp += "  >>> readtime = " + \
        "data / (100*1024*1024) / 60.0 / 60.0 # [h] (at 100 MB/sec)\n"
    myhelp += "  >>> sumtime = max(copytime,calculatechecksumtime) + " + \
        "max(readtime,calculatechecksumtime) # [h]\n"
    myhelp += "  >>> sumtime\n"
    myhelp += "  5.825422222222222\n\n"
    myhelp += "By using md5sum instead of sha256 you can speed up the " + \
        "calculatechecksumtime,\n"
    myhelp += "e. g.:\n"
    myhelp += "  >>> calculatechecksumtime = " + \
        "data/(150*1024*1024)/60.0/60.0 # [h] (at 150 MB/sec with sha256sum)\n"
    myhelp += "  >>> calculatechecksumtime\n"
    myhelp += "  1.9418074074074074\n"
    myhelp += "  >>> calculatechecksumtime = " + \
        "data/(480*1024*1024)/60.0/60.0 # [h] (at 480 MB/sec with md5sum)\n"
    myhelp += "  >>> calculatechecksumtime\n"
    myhelp += "  0.6068148148148148\n\n"
    myhelp += "But still copytime and readtime are limiting the process:\n"
    myhelp += "  >>> copytime\n"
    myhelp += "  2.912711111111111\n"
    myhelp += "  >>> readtime\n"
    myhelp += "  2.912711111111111\n\n"
    myhelp += "A test on a computer (i5-4590S, 16 GB RAM, source: " + \
        "RAID0 of 3 SSDs MZ-75E500B,\n"
    myhelp += "destinations: 2 HDs WD10JFCX) with 745 GB needs 5.6 hours.\n"
    myhelp += "This means it takes about 7.7 h/TB. " + \
        "This correspond to a read/write\n"
    myhelp += "performance of 75 MB/sec.\n"
    myhelp += "A test on a computer (i5-4590S, 16 GB RAM, source: " + \
        "RAID0 of 3 SSDs MZ-75E500B,\n"
    myhelp += "destinations: " + \
        "2 HDs WD20NPVX-00EA4T0) with 1.3 TB needs 10.5 hours.\n"
    myhelp += "This means it takes about 8.1 h/TB. " + \
        "This correspond to a read/write\n"
    myhelp += "performance of 72 MB/sec."
    epilog = "Author: Daniel Mohr\n"
    epilog += "Date: %s\n" % __date__
    epilog += "License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.\n"
    epilog += "\n%s" % myhelp
    description = 'This is the command to copy/replicate data/files ' + \
        'from one directory to other directories (one or more). '
    description += 'It uses the command line programs ' + \
        'e. g. "rsync" and "sha256sum". '
    description += 'Although we use by default rsync, ' + \
        'the source and destination paths have to be local. '
    description += 'If copy is done by "rsync" and this script is run on ' + \
        'a windows system, the drive letters will be replaces ' + \
        'by "/cygdrive/[drive letter]/". '
    description += 'All (long) options can be abbreviated to a prefix, ' + \
        'if the abbreviation is unambiguous ' + \
        '(the prefix matches a unique option) -- e. g. "-dest" or "-de" ' + \
        'instead of "-destination".'
    parser = subparsers.add_parser(
        'replicate',
        description=description,
        help='This is the command to copy/replicate data/files from ' +
        'one directory to other directories (one or more). ' +
        'For more help: pfu replicate -h',
        epilog="%s" % epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.set_defaults(func=replicate)
    parser.add_argument(
        '-source',
        nargs=1,
        default="",
        type=str,
        required=True,
        dest='source',
        help='source directory',
        metavar='dir')
    parser.add_argument(
        '-destination',
        nargs="+",
        default="",
        type=str,
        required=True,
        dest='destination',
        help='destination directory/directories',
        metavar='dir')
    parser.add_argument(
        '-copy_program1',
        nargs=1,
        default="rsync",
        type=str,
        required=False,
        dest='copy_program1',
        help='The program to use for copy in first step. ' +
        'If you use cp instead of rsync, the destination directories ' +
        'should not exist. default: rsync',
        metavar='prg')
    parser.add_argument(
        '-copy_parameter1',
        nargs=1,
        default="--archive --update --one-file-system --links " +
        "--hard-links --sparse",
        type=str,
        required=False,
        dest='copy_parameter1',
        help='Parameter for the copy program in first step. ' +
        'If you use cp instead of rsync, the parameter ' +
        '"--recursive --archive --update --one-file-system ' +
        '--no-dereference" could be used. ' +
        'default: "--archive --update --one-file-system --links ' +
        '--hard-links --sparse"',
        metavar='param')
    parser.add_argument(
        '-copy_program2',
        nargs=1,
        default="rsync",
        type=str,
        required=False,
        dest='copy_program2',
        help='The program to use for copy in second step. default: rsync',
        metavar='prg')
    parser.add_argument(
        '-copy_parameter2',
        nargs=1,
        default="--archive --update --one-file-system --links --hard-links " +
        "--sparse",
        type=str,
        required=False,
        dest='copy_parameter2',
        help='Parameter for the copy program in second step. ' +
        'default: "--archive --update --one-file-system --links ' +
        '--hard-links --sparse"',
        metavar='param')
    parser.add_argument(
        '-checksum_program',
        nargs=1,
        default="sha256sum",
        type=str,
        required=False,
        dest='checksum_program',
        help='Program to calculate the checksums. default: sha256sum',
        metavar='prg')
    parser.add_argument(
        '-checksum_create_parameter',
        nargs=1,
        default="--tag --",
        type=str,
        required=False,
        dest='checksum_create_parameter',
        help='Parameter uses for the program (e. g. sha256sum) to ' +
        'create checksums. default: "--tag --"',
        metavar='param')
    parser.add_argument(
        '-checksum_check_parameter',
        nargs=1,
        default="--check",
        type=str,
        required=False,
        dest='checksum_check_parameter',
        help='Parameter uses for the program (e. g. sha256sum) to ' +
        'check checksums. default: "--quiet --check"',
        metavar='param')
    parser.add_argument(
        '-checksum_check_method',
        nargs=1,
        default=0,
        type=int,
        required=False,
        choices=[0, 1],
        dest='checksum_check_method',
        help='Chose the method. 0: Check the checksums in the destination ' +
        'by the program creating checksums. 1: Do not check the checksums, ' +
        'but instead calculate new ones in the file given by the flag ' +
        '"-checksum_file_name_destination" (see below). You have to set ' +
        '"-checksum_check_parameter" appropriate, ' +
        'e. g. "-checksum_check_parameter \' --tag\'". default: 0',
        metavar='m')
    parser.add_argument(
        '-overwrite_checksum_file',
        nargs=1,
        default=0,
        type=int,
        required=False,
        choices=[0, 1, 2],
        dest='overwrite_checksum_file',
        help='Normally the checksums are only calculated in the source ' +
        'directory, if they do not exist. If set to 1, existing checksum ' +
        'files will be overwritten in the source directories. ' +
        'By setting this value to 2 the missing checksums are calculated; ' +
        'already existing checksums are not verified; ' +
        'it is expected a BSD-style checksum in the checksum file. default: 0',
        metavar='i')
    parser.add_argument(
        '-checksum_file_name',
        nargs=1,
        default=".checksum",
        type=str,
        required=False,
        dest='checksum_file_name',
        help='Name of the checksum file, which will be created in every ' +
        'subdirectory (of source and will be copied to destination(s)). ' +
        'default: .checksum',
        metavar='f')
    parser.add_argument(
        '-checksum_file_name_destination',
        nargs=1,
        default=".checksum_destination",
        type=str,
        required=False,
        dest='checksum_file_name_destination',
        help='Name of the checksum file for "-checksum_check_method 1", ' +
        'which will be created in every subdirectory (of destination(s)). ' +
        'default: .checksum_destination',
        metavar='f')
    parser.add_argument(
        '-checksum_log_file_name',
        nargs=1,
        default=".checksum.%date.log",
        type=str,
        required=False,
        dest='checksum_log_file_name',
        help='Name of the checksum log file, which will be created in ' +
        'every subdirectory in destination(s) during checking checksums. ' +
        'default: .checksum.%%date.log',
        metavar='f')
    parser.add_argument(
        '-checksum_status_file_name',
        nargs=1,
        default=".checksum.status",
        type=str,
        required=False,
        dest='checksum_status_file_name',
        help='Name of the checksum status file, which will be created in ' +
        'every subdirectory in destination(s) during checking checksums. ' +
        'default: .checksum.status',
        metavar='f')
    parser.add_argument(
        '-use_relpath',
        nargs=1,
        default=1,
        type=int,
        required=False,
        dest='use_relpath',
        choices=[0, 1],
        help='If set to 1, convert the given paths ' +
        '(source and destination(s)) to relative paths. ' +
        'For copy program still absolute paths will be created. default: 1',
        metavar='i')
    parser.add_argument(
        '-use_normcase',
        nargs=1,
        default=1,
        type=int,
        required=False,
        dest='use_normcase',
        choices=[0, 1],
        help='If set to 1, normalize the case of the pathnames ' +
        '(source and destination(s)). default: 1',
        metavar='i')
    parser.add_argument(
        '-use_normpath',
        nargs=1,
        default=1,
        type=int,
        required=False,
        dest='use_normpath',
        choices=[0, 1],
        help='If set to 1, normalize the pathnames by collapsing ' +
        'redundant separators and up-level references ' +
        '(source and destination(s)). default: 1',
        metavar='i')
    parser.add_argument(
        '-number_of_processes',
        nargs=1,
        default=4,
        type=int,
        required=False,
        dest='number_of_processes',
        help='Number of processes to run in parallel. default: 4',
        metavar='i')
    parser.add_argument(
        '-limit_number_of_processes_to_distinations',
        nargs=1,
        default=1,
        type=int,
        required=False,
        choices=[0, 1],
        dest='limit_number_of_processes_to_distinations',
        help='Since the read speed of the data is dominating the ' +
        'calculation/processing time, by default (set to 1) only ' +
        '1 process is started per destination. By setting this flag to ' +
        '0 this limitation is canceled. default: 1',
        metavar='i')
    parser.add_argument(
        '-sleeptime',
        nargs=1,
        default=0.1,
        type=float,
        required=False,
        choices=[0, 1],
        dest='sleeptime',
        help='Number of seconds to sleep between checking running ' +
        'subprocesses. default: 0.1',
        metavar='f')
    parser.add_argument(
        '-extrasleeptime',
        nargs=1,
        default=1.0,
        type=float,
        required=False,
        dest='extrasleeptime',
        help='Number of seconds to sleep between steps (2 times). ' +
        'default: 1.0',
        metavar='f')
    parser.add_argument(
        '-dryrun',
        nargs=1,
        default=0,
        type=int,
        required=False,
        choices=[0, 1],
        dest='dryrun',
        help='If set to 1 nothing will be done. default: 0',
        metavar='i')
    create_common_parameter(parser)
