"""
Author: Daniel Mohr.

Date: 2017-03-07, 2021-05-25 (last change).

License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import base64
import hashlib
import logging
import os

import pfu_module.checksum_tools  # own_logger
from pfu_module.checksum_tools import read_data_from_file


class CreateChecksumsClass(object):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2017-03-07, 2021-05-25 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

    class to create checksums in directory or directories
    """
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments

    def __init__(self,
                 directories=(),
                 algorithm='sha512',
                 coding='base64',
                 store='dir',
                 ignore=[".md5", ".sha256", ".sha512"],
                 buf_size=524288,  # 1024*512 Bytes = 512 kB
                 chunk_size=12582912,  # 12 MB
                 create_only_missing=1,
                 level=20,
                 hash_file_prefix='.checksum'):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@dlr.de
        :Date: 2017-03-06 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

        class to create checksums in directory or directories

        :param directories: Create hashes for this list of directories.
                            Symbolic links in given directories are ignored.
        :param algorithm: Set the algorithm used to calculate the hashes.
        :param coding: Set the coding format (RFC 3548) of the hash output.
        :param store: Set the file(s) to store the hashes.
                      Set to \"dir\" means store the hashes in a file for
                      every directory. Set to \"single\" means store the hashes
                      in a single file (for every given directory). Set to
                      \"many\" means store the hashes in a file for every data
                      file.
        :param ignore: list of file extensions, which are ignored
        :param buf_size: Files will be read in chunks of the given amount of
                         Bytes. This should be a factor of the data handled by
                         the hash function (e. g. 64 Bytes for md5, 64 Bytes
                         for sha256, 128 Bytes for sha512).
        :param chunk_size: Set the chunk size. For every n Bytes an own
                           checksum is calculated.
        :param create_only_missing: If set to 1 only missing checksums are
                                    created. A checksum is missing, if the
                                    expected file from store is not available.
                                    If set to 0 hash files are overwritten if
                                    exists.
        :param level: Set how verbose should be the output. This is the level
                      of logging. Lower numbers give more output. The parameter
                      is a number between 1 and 50.
        :param hash_file_prefix: Set the hash file prefix.
        """
        self.level = level
        self.algorithm = algorithm
        self.coding = coding
        self.directories = directories
        self.chunk_size = chunk_size
        self.store = store
        self.hash_file_prefix = hash_file_prefix
        self.create_only_missing = create_only_missing
        self.ignore = ignore
        self.buf_size = buf_size
        self.created_hash_files = []  # list of already created hash files
        self.log = logging.getLogger("pfu.create")
        self.log.setLevel(1)
        self.hashfkt = {'sha512': hashlib.sha512,
                        'sha256': hashlib.sha256,
                        'md5': hashlib.md5}[self.algorithm]
        #self.hashfkt = None
        # if self.algorithm == 'sha512':
        #    self.hashfkt = hashlib.sha512
        # elif self.algorithm == 'sha256':
        #    self.hashfkt = hashlib.sha256
        # elif self.algorithm == 'md5':
        #    self.hashfkt = hashlib.md5
        #self.encode = None
        # if self.coding in ['hex', 'Base16']:
        #    self.encode = base64.b16encode
        # elif self.coding in ['base32', 'Base32']:
        #    self.encode = base64.b32encode
        # elif self.coding in ['base64', 'Base64']:
        #    self.encode = base64.b64encode
        self.encode = {'hex': base64.b16encode,
                       'base16': base64.b16encode,
                       'Base16': base64.b16encode,
                       'base32': base64.b32encode,
                       'Base32': base64.b32encode,
                       'base64': base64.b64encode,
                       'Base64': base64.b64encode}[self.coding]

    def calculate_hash(self, data_file_name):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@dlr.de
        :Date: 2016-12-08, 2021-05-25 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

        Calculate hash(es) for data_file_name

        :param data_file_name: file name of the file to analyse
        """
        out = [()]
        with open(data_file_name, 'rb') as data_file:
            last_position = 0
            cal_hash = self.hashfkt()
            create_chunk_hashes = False
            if self.chunk_size < os.path.getsize(data_file_name):
                create_chunk_hashes = True
            filename = os.path.normpath(data_file_name)
            if self.store != 'single':
                filename = os.path.split(data_file_name)[1]
            while data_file.tell() < os.path.getsize(data_file_name):
                hash_objects = [cal_hash]
                if create_chunk_hashes:
                    cal_chunk_hash = self.hashfkt()
                    hash_objects += [cal_chunk_hash]
                read_data_from_file(self.buf_size, data_file,
                                    self.chunk_size, hash_objects)
                if create_chunk_hashes:
                    out += [(self.encode(cal_chunk_hash.digest()).decode(),
                             '  ',
                             filename,
                             ' (bytes ', '%i' % last_position,
                             ' - ',
                             '%i' % (data_file.tell()-1), ')')]
                last_position = data_file.tell()
            out[0] = (self.encode(cal_hash.digest()).decode(),
                      '  ',
                      filename)
        return out

    def _calculate_store_hash(self, data_file_name, hash_file_name):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@dlr.de
        :Date: 2017-03-07 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

        Calculate hash and store hash in file and list.
        This method should not be called from outside.
        If IOError occurred during hashing the file data_file_name,
        no hashes are stored.

        :param data_file_name: file name of the file to analyse
        :param hash_file_name: file name of the file to store hash
        """
        err = 0  # no error
        # calculate hash for data_file_name
        try:
            out = self.calculate_hash(data_file_name)
        except IOError:
            err = 1  # IOError
            self.log.warning(
                'IOError during hashing file "%s"', data_file_name)
        if err == 0:
            # store hash in hash_file_name
            with open(hash_file_name, 'a') as hash_file:
                for line in out:
                    hash_file.write(''.join(line)+"\n")
                self.log.verboseinfo(
                    "file \"%s\": write %i hashes", data_file_name, len(out))
            # store hash file name in list
            if hash_file_name not in self.created_hash_files:
                self.created_hash_files += [hash_file_name]

    def create_checksum(self, dirpath, data_file_name):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@dlr.de
        :Date: 2017-02-25 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

        Create hashes for the file name.

        :param dirpath: directory of the file
        :param data_file_name: file name of the file to analyse
        """
        if (os.path.isfile(data_file_name) and
                os.access(data_file_name, os.R_OK)):
            hash_file_name = ""
            if self.store == 'dir':
                hash_file_name = os.path.join(
                    dirpath,
                    self.hash_file_prefix + '.' + self.algorithm)
            elif self.store == 'single':
                hash_file_name = self.hash_file_prefix + '.' + self.algorithm
            elif self.store == 'many':
                hash_file_name = data_file_name + '.' + self.algorithm
            self.log.debug("possible write hash to \"%s\"", hash_file_name)
            if ((self.create_only_missing == 0) or
                    (not os.path.exists(hash_file_name)) or
                    (hash_file_name in self.created_hash_files)):
                if ((self.create_only_missing == 0) and
                        os.path.exists(hash_file_name) and
                        (hash_file_name not in self.created_hash_files)):
                    os.remove(hash_file_name)
                self._calculate_store_hash(data_file_name, hash_file_name)
            elif (os.path.exists(hash_file_name) and
                  (hash_file_name not in self.created_hash_files)):
                self.log.debug(
                    "hash file \"%s\" already exists", hash_file_name)
            else:
                self.log.debug(
                    "hash file \"%s\" not used (no reason)", hash_file_name)
        elif not os.access(data_file_name, os.R_OK):
            self.log.warning('file "%s" is not readable', data_file_name)
        else:
            self.log.warning('file "%s" not existing (anymore?)',
                             data_file_name)

    def is_hash_file(self, name):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@dlr.de
        :Date: 2016-12-02 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

        Determine if name is a hash file.

        :param name: name of the file
        """
        ret = False
        for file_extention in self.ignore:
            if name.endswith(file_extention):
                ret = True
                break
        return ret

    def create_hashes_in_directory(self, name):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@dlr.de
        :Date: 2017-02-25 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

        Create hashes for every file in this directory.

        :param name: name of the top directory to handle
        """
        self.log.debug("analyse directory \"%s\"", name)
        self.created_hash_files = []  # list of already created hash files
        for (dirpath, _, filenames) in os.walk(name):
            for filename in filenames:
                if not self.is_hash_file(os.path.join(dirpath, filename)):
                    self.log.debug("create hash for file \"%s\"",
                                   os.path.join(dirpath, filename))
                    self.create_checksum(
                        dirpath,
                        os.path.join(dirpath, filename))

    def create_all(self):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@dlr.de
        :Date: 2017-02-25 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

        create (missing) checksums
        """
        for name in self.directories:
            if os.path.isdir(name):
                self.create_hashes_in_directory(name)
            else:
                self.log.warning(
                    "cannot handle '%s' (e. g. not a directory)", name)
        return 0  # success
