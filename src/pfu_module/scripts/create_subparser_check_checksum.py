"""
Author: Daniel Mohr.
Date: 2017-03-01 (last change).
License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import argparse

from .create_common_parameter import create_common_parameter

__date__ = "2017-03-01"


def check_checksum(args):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2017-02-13 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

    This function should check checksums.

    :param args: command line arguments given in a structure from argparse
    """
    # pylint: disable=invalid-name
    import pfu_module.check_checksum
    c = pfu_module.check_checksum.CheckChecksumsClass(
        directories=args.directories,
        hash_extension=args.hash_extension,
        ignore_extension=args.ignore_extension,
        buf_size=args.buf_size[0],
        level=args.loglevel[0])
    return c.check_all()


def create_subparser_check_checksum(subparsers):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2017-03-01 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
    """
    # pylint: disable=line-too-long
    myprehelp = "This command will check checksums. "
    myprehelp += "We assume relative paths in each hash file. "
    myprehelp += "Command line parameters can be shortened, "
    myprehelp += "as far as they are unique."
    myposthelp = "Example:\n\n"
    myposthelp += " pfu check_checksum -d . -loglevel 15 -logfile output.log\n"
    myposthelp += " pfu check_checksum -d . -loglevel 15 "
    myposthelp += "-i \"~\" .tmp .bak .md5\n"
    myposthelp += " pfu check_checksum -directory . -loglevel 20"
    parser = subparsers.add_parser(
        'check_checksum',
        description=myprehelp,
        help=myprehelp+' For more help: pk4_checksums.py check -h',
        epilog="Author: Daniel Mohr.\nDate: %s.\nLicense: " % __date__ +
        "GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.\n\n" +
        "%s" % myposthelp,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '-directory',
        nargs="+",
        default=[""],
        type=str,
        required=True,
        dest='directories',
        help='Check hashes for this directory tree or these directory trees.' +
        ' Symbolic links in given directories are ignored. ' +
        'All hash files and data files have to be in this directory tree or ' +
        'these directory trees.',
        metavar='dir')
    parser.add_argument(
        '-hash_extension',
        nargs="+",
        default=[".md5", ".sha256", ".sha512", ".checksum", ".sha1"],
        type=str,
        dest='hash_extension',
        help='Files with the given extension(s) are interpreted as ' +
        'hash files. The files have to be of the format ' +
        'r"(?P<hash>[0-9a-zA-Z/+=]+) [ \*]{1}(?P<filename>.+) ' +  # noqa
        '\(bytes (?P<start>[0-9]+) - (?P<stop>[0-9]+)\)$", ' +  # noqa
        'r"(?P<hash>[0-9a-zA-Z/+=]+) [ \*]{1}(?P<filename>.+)$" or ' +  # noqa
        'r"(?P<type>MD5|SHA256|SHA512|SHA1|SHA224|SHA384)[ ]{0,1}' +  # noqa
        '\((?P<filename>.+)\)[ ]{0,1}= (?P<hash>[0-9a-zA-Z/+=]+)$". ' +  # noqa
        'In the latter case base16 encoding is assumed. ' +
        'The hash types sha1, sha224 and sha384 are only interpreted/used ' +
        'for the BSD-style. default: .md5 .sha256 .sha512 .checksum .sha1',
        metavar='ext')
    parser.add_argument(
        '-ignore_extension',
        nargs="+",
        default=["~", ".tmp", ".bak"],
        type=str,
        dest='ignore_extension',
        help='Files with the given extension(s) are ignored. ' +
        'default: ~ .tmp .bak',
        metavar='ext')
    parser.add_argument(
        '-buf_size',
        nargs=1,
        default=[524288],  # 1024*512 Bytes = 512 kB
        type=int,
        required=False,
        dest='buf_size',
        help='Files will be read in chunks of the given amount of Bytes. ' +
        'This should be a factor of the data handled by the hash function ' +
        '(e. g. 64 Bytes for md5, 64 Bytes for sha256, ' +
        '128 Bytes for sha512). default (512 kB): 524288',
        metavar='i')
    create_common_parameter(parser)
    parser.set_defaults(func=check_checksum)
