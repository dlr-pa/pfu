"""
Author: Daniel Mohr.
Date: 2017-02-25 (last change).
License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import argparse

from .create_common_parameter import create_common_parameter

__date__ = "2017-02-13"

def create_checksum(args):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2017-02-13 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

    This function should create (missing) checksums.

    :param args: command line arguments given in a structure from argparse
    """
    # pylint: disable=invalid-name
    import pfu_module.create_checksum
    c = pfu_module.create_checksum.CreateChecksumsClass(
        directories=args.directories,
        algorithm=args.algorithm[0],
        coding=args.coding[0],
        store=args.store[0],
        ignore=args.ignore,
        buf_size=args.buf_size[0],
        chunk_size=args.chunk_size[0],
        create_only_missing=args.create_only_missing[0],
        level=args.loglevel[0],
        hash_file_prefix=args.hash_file_prefix[0])
    return c.create_all()

def check_chunk_size(value):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2016-12-08 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
    """
    # pylint: disable=redefined-variable-type
    ivalue = 0
    if value.lower() == 'inf':
        ivalue = float('inf')
    else:
        ivalue = int(value)
        if ivalue < 1:
            raise argparse.ArgumentTypeError(
                "%s is an invalid positive int value (it is also not inf)" % value)
    return ivalue

def create_subparser_create_checksum(subparsers):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2017-02-25 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
    """
    # pylint: disable=line-too-long
    # pylint: disable=invalid-name
    help_create = ""
    help_create += "This command will create (missing) checksums. Command line parameters can be shortened, as far as they are unique."
    myposthelp = "Example:\n\n"
    myposthelp += " pfu create_checksum -d .\n"
    myposthelp += " pfu create_checksum -d . -logfile l -fileloglevel 15"
    parser_create = subparsers.add_parser(
        'create_checksum',
        description=help_create,
        help=help_create+' For more help: pfu create_checksum -h',
        epilog="Author: Daniel Mohr.\nDate: %s.\nLicense: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.\n\n%s" % (__date__, myposthelp),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser_create.add_argument(
        '-directory',
        nargs="+",
        default=[""],
        type=str,
        required=True,
        dest='directories',
        help='Create hashes for this directory tree or these directory trees. Symbolic links in given directories are ignored.',
        metavar='dir')
    parser_create.add_argument(
        '-algorithm',
        nargs=1,
        default=['sha512'],
        choices=['md5', 'sha256', 'sha512'],
        type=str,
        required=False,
        dest='algorithm',
        help='Set the algorithm used to calculate the hashes. Possible values are: md5, sha256, sha512. default: sha512',
        metavar='a')
    parser_create.add_argument(
        '-coding',
        nargs=1,
        default=['base64'],
        choices=['hex', 'base16', 'base32', 'base64', 'Base16', 'Base32', 'Base64'],
        type=str,
        required=False,
        dest='coding',
        help='Set the coding format (RFC 3548) of the hash output. Possible values are: hex (alias for base16), base16, base32, base64. default: base64',
        metavar='c')
    parser_create.add_argument(
        '-store',
        nargs=1,
        default=['dir'],
        choices=['dir', 'single', 'many'],
        type=str,
        required=False,
        dest='store',
        help='Set the file(s) to store the hashes. Set to \"dir\" means store the hashes in a file for every directory. Set to \"single\" means store the hashes in a single file (for every given directory). Set to \"many\" means store the hashes in a file for every data file. default: dir',
        metavar='p')
    parser_create.add_argument(
        '-ignore',
        nargs="+",
        default=[".md5", ".sha256", ".sha512"],
        type=str,
        dest='ignore',
        help='Files with the given extension(s) are ignored (interpreted as hash files). default: .md5 .sha256 .sha512',
        metavar='ext')
    parser_create.add_argument(
        '-buf_size',
        nargs=1,
        default=[524288], # 1024*512 Bytes = 512 kB
        type=int,
        required=False,
        dest='buf_size',
        help='Files will be read in chunks of the given amount of Bytes. This should be a factor of the data handled by the hash function (e. g. 64 Bytes for md5, 64 Bytes for sha256, 128 Bytes for sha512). default (512 kB): 524288',
        metavar='i')
    parser_create.add_argument(
        '-chunk_size',
        nargs=1,
        default=[12582912],
        type=check_chunk_size,
        required=False,
        dest='chunk_size',
        help='Set the chunk size. For every n Bytes an own checksum is calculated. If you want no checksums for chunks you can set this value to "inf". default (12 MB): 12582912',
        metavar='n')
    parser_create.add_argument(
        '-create_only_missing',
        nargs=1,
        default=[1],
        choices=[0, 1],
        type=int,
        required=False,
        dest='create_only_missing',
        help='If set to 1 only missing checksums are created. A checksum is missing, if the expected file from store is not available. If set to 0 hash files are overwritten if exists. default: 1',
        metavar='n')
    parser_create.add_argument(
        '-hash_file_prefix',
        nargs=1,
        default=['.checksum'],
        type=str,
        required=False,
        dest='hash_file_prefix',
        help='Set the hash file prefix. default: .checksum',
        metavar='f')
    create_common_parameter(parser_create)
    parser_create.set_defaults(func=create_checksum)
