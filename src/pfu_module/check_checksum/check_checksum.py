"""
Author: Daniel Mohr.

Date: 2017-03-07, 2021-05-25 (last change).

License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import base64
import copy
import hashlib
import logging
import os
import re

# own_logger:
import pfu_module.checksum_tools  # pylint: disable=unused-import

from pfu_module.checksum_tools import read_data_from_file


class CheckChecksumsClass(object):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2017-03-07, 2021-05-25 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

    class to check checksums in directory or directories
    """
    # pylint: disable=too-many-instance-attributes
    hashfcts = {'sha512': hashlib.sha512,
                'sha256': hashlib.sha256,
                'md5': hashlib.md5,
                'sha1': hashlib.sha1,
                'sha224': hashlib.sha224,
                'sha384': hashlib.sha384}
    encodes = {'hex': base64.b16encode,
               'base16': base64.b16encode,
               'Base16': base64.b16encode,
               'base32': base64.b32encode,
               'Base32': base64.b32encode,
               'base64': base64.b64encode,
               'Base64': base64.b64encode}
    hashtype = {128: ('sha512', 'base16'),
                104: ('sha512', 'base32'),
                88: ('sha512', 'base64'),
                64: ('sha256', 'base16'),
                56: ('sha256', 'base32'),
                44: ('sha256', 'base64'),
                32: ('md5', 'base16 or base32'),
                24: ('md5', 'base64')}
    regexps = [
        re.compile(
            r"(?P<hash>[0-9a-zA-Z/+=]+) [ \*]{1}(?P<filename>.+) \(bytes (?P<start>[0-9]+) - (?P<stop>[0-9]+)\)$"),
        re.compile(r"(?P<hash>[0-9a-zA-Z/+=]+) [ \*]{1}(?P<filename>.+)$"),
        re.compile(r"(?P<type>MD5|SHA256|SHA512|SHA1|SHA224|SHA384)[ ]{0,1}\((?P<filename>.+)\)[ ]{0,1}= (?P<hash>[0-9a-zA-Z/+=]+)$")]

    def __init__(self,
                 directories=(),
                 hash_extension=[".md5", ".sha256", ".sha512"],
                 ignore_extension=["~", ".tmp", ".bak"],
                 buf_size=524288,  # 1024*512 Bytes = 512 kB
                 level=20):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@dlr.de
        :Date: 2017-02-25 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

        class to create checksums in directory or directories

        :param directories: Create hashes for this list of directories.
                            Symbolic links in given directories are ignored.
        :param hash_extension: Files with the given extension(s) are interpreted
                               as hash files.
        :param ignore_extension: Files with the given extension(s) are ignored
        :param buf_size: Files will be read in chunks of the given amount of
                         Bytes. This should be a factor of the data handled by
                         the hash function (e. g. 64 Bytes for md5, 64 Bytes
                         for sha256, 128 Bytes for sha512).
        :param level: Set how verbose should be the output. This is the level
                      of logging. Lower numbers give more output. The parameter
                      is a number between 1 and 50.
        """
        # pylint: disable=too-many-arguments
        self.directories = directories
        hash_extension = set(hash_extension)
        self.ignore_extension = set(ignore_extension)
        self.accept_hash_extension = hash_extension - self.ignore_extension
        self.not_file_extension = hash_extension & self.ignore_extension
        self.buf_size = buf_size
        self.level = level
        self.log = logging.getLogger("pfu.check")
        self.log.setLevel(1)
        self.hash_files = []
        self.data_files = []
        self.hash_dicts = [dict(), dict()]
        self.result_number = {'data file without hash': 0,
                              'hash without data file': 0,
                              'data file with matching hash(es)': 0,
                              'data file with not matching hash(es)': 0,
                              'hash for ignored file': 0,
                              'data file not handled': 0}

    def determine_hash_encode(self, hash_string, hashfilename=None):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@dlr.de
        :Date: 2017-03-02 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

        Try to determine hash function and encode from hash.
        If this is not possible assume the file extension gives the hash type.

        :param hash_string: the hash to analyse
        :param hashfilename: file name of the hash
                             (if hash is not unique the file extension is used)

        :return: tuple of hash algorithm and encoding
                 or None on error
        """
        hash_encode = None
        if len(hash_string) in self.hashtype:
            hash_encode = self.hashtype[len(hash_string)]
            if hash_encode[1] == 'base16 or base32':
                if hash_string[-6:] == '======':
                    hash_encode = (hash_encode[0], 'base32')
                else:
                    hash_encode = (hash_encode[0], 'base16')
        if (hash_encode is None) and (hashfilename is not None):
            extension = os.path.splitext(hashfilename)[1][1:].strip().lower()
            if extension in self.hashfcts:
                # assume file extension gives the hash type
                # the coding is really hard to detect, therefore assume base16
                # RFC 3548 defines the following alphabets:
                # base64: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_
                # base32: abcdefghijklmnopqrstuvwxyz234567
                # base16: 0123456789ABCDEF
                # Unfortunately typical used tools like *sum (e. g. md5sum)
                # gives the output as base16 in lower letters.
                hash_encode = (extension, 'base16')
        return hash_encode

    def is_accept_hash_file(self, filename):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@dlr.de
        :Date: 2016-12-03 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

        :param filename: filename to analyse

        :return: True, if file extension indicates a hash file
        """
        ret = False
        for file_extention in self.accept_hash_extension:
            if filename.endswith(file_extention):
                ret = True
                break
        return ret

    def is_accept_data_file(self, filename):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@dlr.de
        :Date: 2016-12-03 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

        :param filename: filename to analyse

        :return: True, if file extension indicates a data file
        """
        ret = True
        for file_extention in self.not_file_extension:
            if filename.endswith(file_extention):
                ret = False
        return ret

    def is_accept_data_file2(self, filename):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@dlr.de
        :Date: 2016-12-03 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

        It is assumed the file is not a hash file.

        :param filename: filename to analyse

        :return: True, if file extension indicates a data file
        """
        ret = True
        for file_extention in self.ignore_extension:
            if filename.endswith(file_extention):
                ret = False
        return ret

    def find_all_files(self, name):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@dlr.de
        :Date: 2016-12-08 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

        go to the directory tree and analyse the files

        :param name: name of the top level directory
        """
        self.log.info("analyse directory tree \"%s\" resolved here to \"%s\"",
                      name, os.path.abspath(name))
        self.hash_files = []
        self.data_files = []
        for (dirpath, _, filenames) in os.walk(name):
            for filename in filenames:
                absfilename = os.path.normpath(os.path.join(dirpath, filename))
                if self.is_accept_hash_file(absfilename):
                    self.hash_files += [absfilename]
                elif self.is_accept_data_file2(absfilename):
                    self.data_files += [absfilename]

    def _analyse_hashline_of_chunk(self, sres, hashfilename):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@dlr.de
        :Date: 2017-03-02 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

        Analyse line of a hash file describing hash of a chunk.
        This method should not be called from outside.

        :param sres: re instance
        :param hashfilename: file name of the hash
                             (normaly only path is used, if hash is not unique
                             the file extension is used)
        """
        hash_encode = self.determine_hash_encode(sres.group('hash'),
                                                 hashfilename)
        if hash_encode is not None:
            relfilename = os.path.normpath(
                os.path.join(os.path.dirname(hashfilename),
                             sres.group('filename')))
            if hash_encode[1] == 'base64':
                hash_string = sres.group('hash')
            else:
                hash_string = sres.group('hash').lower()
            if relfilename in self.hash_dicts[0]:
                self.hash_dicts[0][relfilename] += [(
                    hash_string,
                    hash_encode,
                    hashfilename,
                    int(sres.group('start')),
                    int(sres.group('stop')))]
            else:
                self.hash_dicts[0][relfilename] = [(
                    hash_string,
                    hash_encode,
                    hashfilename,
                    int(sres.group('start')),
                    int(sres.group('stop')))]

    def _analyse_hashline_of_file(self, sres, hashfilename):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@dlr.de
        :Date: 2017-03-02 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

        Analyse line of a hash file describing hash of complete file.
        This method should not be called from outside.

        :param sres: re instance
        :param hashfilename: file name of the hash
                             (normaly only path is used, if hash is not unique
                             the file extension is used)
        """
        hash_encode = self.determine_hash_encode(sres.group('hash'),
                                                 hashfilename)
        if hash_encode is not None:
            relfilename = os.path.normpath(
                os.path.join(
                    os.path.dirname(hashfilename),
                    sres.group('filename')))
            if hash_encode[1] == 'base64':
                hash_string = sres.group('hash')
            else:
                hash_string = sres.group('hash').lower()
            if relfilename in self.hash_dicts[1]:
                self.hash_dicts[1][relfilename] += [(
                    hash_string,
                    hash_encode,
                    hashfilename)]
            else:
                self.hash_dicts[1][relfilename] = [(
                    hash_string,
                    hash_encode,
                    hashfilename)]

    def _analyse_hashline_of_file_bsd(self, sres, hashfilename):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@dlr.de
        :Date: 2017-03-01 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

        Analyse line of a hash file describing hash of complete file in
        BSD-style.
        This method should not be called from outside.

        :param sres: re instance
        :param hashfilename: file name of the hash (here only path is used)
        """
        relfilename = os.path.normpath(
            os.path.join(
                os.path.dirname(hashfilename),
                sres.group('filename')))
        if relfilename in self.hash_dicts[1]:
            self.hash_dicts[1][relfilename] += [(
                sres.group('hash').lower(),
                (sres.group('type').lower(), 'base16'),
                hashfilename)]
        else:
            self.hash_dicts[1][relfilename] = [(
                sres.group('hash').lower(),
                (sres.group('type').lower(), 'base16'),
                hashfilename)]

    def read_hash_file(self, hashfilename):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@dlr.de
        :Date: 2017-02-25 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

        read hash file

        :param hashfilename: read this file
        """
        if (os.path.isfile(hashfilename) and
                os.access(hashfilename, os.R_OK)):
            self.log.debug("read hash file \"%s\"", hashfilename)
            with open(hashfilename, 'rU') as hash_file:
                for line in hash_file:
                    sres = self.regexps[0].search(line)
                    if sres:  # hash of a chunk
                        self._analyse_hashline_of_chunk(
                            sres, hashfilename)
                    else:
                        sres = self.regexps[1].search(line)
                        if sres:  # hash of a complete file
                            self._analyse_hashline_of_file(
                                sres, hashfilename)
                        else:
                            sres = self.regexps[2].search(line)
                            if sres:  # hash of a complete file (BSD-style)
                                self._analyse_hashline_of_file_bsd(
                                    sres, hashfilename)
                            else:
                                self.log.warning(
                                    "do not understand line in hash file \"%s\": %s",
                                    hashfilename, line)
        elif not os.access(hashfilename, os.R_OK):
            self.log.warning('hash file "%s" is not readable', hashfilename)
        else:
            self.log.warning('hash file "%s" not existing (anymore?)',
                             hashfilename)

    def read_all_hash_files(self):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@dlr.de
        :Date: 2016-12-03 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

        read all hash files already found by the class
        """
        self.log.debug("read_all_hash_files")
        self.hash_dicts = [dict(), dict()]
        # self.hash_dicts[0][filename]...
        for filename in self.hash_files:
            self.read_hash_file(filename)
        for filename in self.hash_dicts[0]:
            self.hash_dicts[0][filename].sort(key=lambda x: x[3])

    def compare_hashes_for_file(self, filename):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@dlr.de
        :Date: 2017-03-07, 2021-05-25 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

        compare hashes for the given filename

        :param filename: string of the filename
        """
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-branches
        match = True
        number_hashes = 0
        if filename in self.hash_dicts[1]:
            number_hashes = len(self.hash_dicts[1][filename])
        hash_objects = [None] * number_hashes  # global hash objects
        for i in range(number_hashes):
            hash_objects[i] = self.hashfcts[
                self.hash_dicts[1][filename][i][1][0]]()
        number_chunk_hashes = 0
        chunks = []
        if filename in self.hash_dicts[0]:
            number_chunk_hashes = len(self.hash_dicts[0][filename])
            chunks = copy.deepcopy(self.hash_dicts[0][filename])
            # chunks is list of: (hash, (alg, encode), hashfile, start, stop)
        chunk_objects = []
        chunk_objects_index = []
        filesize = os.path.getsize(filename)
        with open(filename, 'rb') as data_file:
            next_pos = None
            while data_file.tell() < filesize:
                act_pos = data_file.tell()
                for (i, chunk) in enumerate(chunks):
                    if act_pos == chunk[3]:
                        if next_pos is None:
                            next_pos = chunk[4]
                        else:
                            next_pos = min(next_pos, chunk[4])
                        chunk_objects += [self.hashfcts[chunk[1][0]]()]
                        chunk_objects_index += [i]
                if next_pos is None:
                    for chunk in chunks:
                        if act_pos < chunk[3]:
                            if next_pos is None:
                                next_pos = chunk[3]
                            else:
                                next_pos = min(next_pos, chunk[3])
                    if next_pos is None:
                        next_pos = filesize-1
                read_data_from_file(
                    self.buf_size,
                    data_file,
                    next_pos + 1 - act_pos,
                    hash_objects + chunk_objects)
                next_pos = None
                act_pos = data_file.tell()-1  # we need one before up to end of while
                i = 0
                while i < len(chunk_objects):
                    if act_pos == chunks[chunk_objects_index[i]][4]:
                        # compare hash
                        encode = self.encodes[chunks[chunk_objects_index[i]][1][1]]
                        cal_hash = encode(
                            chunk_objects[chunk_objects_index[i]].digest())
                        if chunks[chunk_objects_index[i]][1][1] != 'base64':
                            cal_hash = cal_hash.lower()
                        if cal_hash.decode() != chunks[chunk_objects_index[i]][0]:
                            match = False
                            break
                        del chunks[chunk_objects_index[i]]
                        del chunk_objects[chunk_objects_index[i]]
                        del chunk_objects_index[i]
                        for (j, _) in enumerate(chunk_objects_index):
                            if chunk_objects_index[j] >= i:
                                chunk_objects_index[j] -= 1
                    else:
                        if next_pos is None:
                            next_pos = chunks[chunk_objects_index[i]][4]
                        else:
                            next_pos = min(
                                next_pos, chunks[chunk_objects_index[i]][4])
                        i += 1
                if next_pos is not None:
                    act_pos += 1  # it was wrong before
                    for chunk in chunks:
                        if act_pos < chunk[3]:
                            next_pos = min(next_pos, chunk[3])
                if not match:
                    break
        # compare global hash
        for i in range(number_hashes):
            encode = self.encodes[self.hash_dicts[1][filename][i][1][1]]
            cal_hash = encode(hash_objects[i].digest())
            if self.hash_dicts[1][filename][i][1][1] != 'base64':
                cal_hash = cal_hash.lower()
            if cal_hash.decode() != self.hash_dicts[1][filename][i][0]:
                match = False
                break
        return (match, number_hashes, number_chunk_hashes, filesize)

    def analyse_all_files(self):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@dlr.de
        :Date: 2017-02-25 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

        analyse all files and compare hashes
        """
        self.log.debug("analyse_all_files")
        files = list(set(self.hash_dicts[0].keys()) |
                     set(self.hash_dicts[1].keys()) |
                     set(self.data_files))
        files.sort()
        self.result_number = {'data file without hash': 0,
                              'hash without data file': 0,
                              'data file with matching hash(es)': 0,
                              'data file with not matching hash(es)': 0,
                              'hash for ignored file': 0,
                              'data file not handled': 0}
        for filename in files:
            if filename in self.data_files:
                if (((filename in self.hash_dicts[0]) or
                     (filename in self.hash_dicts[1])) and
                        os.path.isfile(filename) and
                        os.access(filename, os.R_OK)):
                    # data file and related hash(es) available
                    (match,
                     number_hashes,
                     number_chunk_hashes,
                     filesize) = self.compare_hashes_for_file(filename)
                    if match:
                        self.result_number['data file with matching hash(es)'] += 1
                        self.log.verboseinfo(  # pylint: disable=no-member
                            'file \"%s\" %i: OK (#hash= %i #chunk_hash= %i)',
                            filename,
                            filesize,
                            number_hashes,
                            number_chunk_hashes)
                    else:
                        self.result_number['data file with not matching hash(es)'] += 1
                        self.log.verboseinfo(  # pylint: disable=no-member
                            'file \"%s\" %i: bad, hash mismatch (some of: #hash= %i #chunk_hash= %i)',
                            filename,
                            filesize,
                            number_hashes,
                            number_chunk_hashes)
                elif not ((filename in self.hash_dicts[0]) or
                          (filename in self.hash_dicts[1])):
                    self.result_number['data file without hash'] += 1
                    self.log.verboseinfo(  # pylint: disable=no-member
                        'file \"%s\": no corresponding hash(es) found',
                        filename)
                else:
                    self.result_number['data file not handled'] += 1
                    if not os.access(filename, os.R_OK):
                        self.log.warning('file "%s" is not readable', filename)
                    if not os.path.isfile(filename):
                        self.log.warning('file "%s" not existing (anymore?)',
                                         filename)
                    else:
                        self.log.warning('cannot handle file "%s"', filename)
            else:
                if os.path.isfile(filename) is True:
                    filesize = os.path.getsize(filename)
                    self.result_number['hash for ignored file'] += 1
                    self.log.verboseinfo(  # pylint: disable=no-member
                        'file \"%s\" % i: ignored, but hash(es) available',
                        filename,
                        filesize)
                else:
                    self.result_number['hash without data file'] += 1
                    self.log.verboseinfo(  # pylint: disable=no-member
                        'file \"%s\": not found, but hash(es) available',
                        filename)

    def check_all(self):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@dlr.de
        :Date: 2017-02-25 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

        check checksums
        """
        for name in self.directories:
            if os.path.isdir(name):
                self.find_all_files(name)
                # now self.hash_files and self.data_files is filled
                self.read_all_hash_files()
                # now self.hash_dicts is filled
                self.analyse_all_files()
                self.log.info(
                    'data file without hash: %i',
                    self.result_number['data file without hash'])
                self.log.info(
                    'hash without data file: %i',
                    self.result_number['hash without data file'])
                self.log.info(
                    'data file with matching hash(es): %i',
                    self.result_number['data file with matching hash(es)'])
                self.log.info(
                    'data file with not matching hash(es): %i',
                    self.result_number['data file with not matching hash(es)'])
                self.log.info(
                    'hash for ignored file: %i',
                    self.result_number['hash for ignored file'])
                self.log.info(
                    'data file not handled (not ignored): %i',
                    self.result_number['data file not handled'])
                #raise NotImplementedError("not finished")
            else:
                self.log.warning(
                    "cannot handle '%s' (e. g. not a directory)", name)
        return 0  # success
