"""
:Author: Daniel Mohr
:Email: daniel.mohr@gmx.de
:Date: 2017-08-23 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import logging
import logging.handlers
import os
import os.path
import pickle
import threading
import time

import pfu_module.SimScrub


class Scrubbing(object):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@gmx.de
    :Date: 2017-08-23 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
    """
    # pylint: disable=too-many-instance-attributes

    def __init__(self,
                 config_dir,
                 semaphore_lock,
                 event_lock,
                 loglevel=1,
                 time_delta=23,
                 chunk_size=524288,
                 reduced_chunk_size=1024,
                 max_retry=3,
                 omit_chunk_size=1024,
                 update=True):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@gmx.de
        :Date: 2017-01-10 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
        """
        # pylint: disable=too-many-arguments
        # store parameter
        self._config_dir = config_dir
        self._semaphore_lock = semaphore_lock
        self._event_lock = event_lock  # is set on finishing
        self._loglevel = loglevel
        self._time_delta = time_delta
        self._chunk_size = chunk_size
        self._reduced_chunk_size = reduced_chunk_size
        self._max_retry = max_retry
        self._omit_chunk_size = omit_chunk_size
        self._update = update
        # create own variables
        self._scrubbing = False
        self._file_status = os.path.join(self._config_dir, 'status')
        self._status = 0
        self._read_status()

    def _read_file(self, file_name, log):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@gmx.de
        :Date: 2017-01-10 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
        """
        if os.path.isfile(file_name) and os.access(file_name, os.R_OK):
            retry = self._max_retry
            chunk_size = self._chunk_size
            with open(file_name, 'rb') as data_file:
                while (self._scrubbing and
                       (data_file.tell() < os.path.getsize(file_name))):
                    try:
                        _ = data_file.read(chunk_size)
                    except IOError:
                        chunk_size = self._reduced_chunk_size
                        retry -= 1
                        if retry <= 0:
                            retry = self._max_retry
                            log.warning(
                                'IOError: cannot read file '
                                '"%s" at %i-%i/%i' % (
                                    file_name,
                                    data_file.tell(),
                                    data_file.tell()+chunk_size-1,
                                    os.path.getsize(file_name)))
                            data_file.seek(
                                min(data_file.tell()+self._omit_chunk_size,
                                    os.path.getsize(file_name)))
                        else:
                            time.sleep(0.1)
                    else:
                        retry = self._max_retry
                        chunk_size = self._chunk_size
        elif not os.access(file_name, os.R_OK):
            log.info('file "%s" is not readable' % file_name)

    def _read_status(self):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@gmx.de
        :Date: 2017-01-06 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
        """
        self._status = 0
        with open(self._file_status, 'rb') as file_desriptor:
            self._status = pickle.load(file_desriptor)

    def _write_status(self, status=None):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@gmx.de
        :Date: 2017-01-06 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
        """
        if status is None:
            status = self._status
        with open(self._file_status, 'wb') as file_desriptor:
            pickle.dump(status, file_desriptor)

    def scrub(self):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@gmx.de
        :Date: 2017-01-06 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
        """
        mythread = threading.Thread(target=self._scrub)
        mythread.start()
        return mythread

    def _do_update(self, log, old_list_of_files):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@gmx.de
        :Date: 2017-08-23 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

        old_list_of_files will be changed to be the new list
        """
        with open(os.path.join(self._config_dir, 'dir'), 'rb') as \
                file_desriptor:
            reldir = pickle.load(file_desriptor)
        new_list_of_files = pfu_module.SimScrub.create_file_list(reldir, log)
        new_set_of_files = set(new_list_of_files)
        new_files = list(new_set_of_files.difference(old_list_of_files))
        old_files = list(set(old_list_of_files).difference(new_set_of_files))
        found_change = False
        if len(old_files) > 0:
            found_change = True
            for filename in old_files:
                index = old_list_of_files.index(filename)
                del old_list_of_files[index]
                if index < self._status:
                    self._status -= 1
        if len(new_files) > 0:
            found_change = True
            old_list_of_files += new_files
        if found_change:
            log.info("updated list of files (%i added, %i deleted)",
                     len(new_files),
                     len(old_files))
            with open(os.path.join(self._config_dir, 'list'),
                      'wb') as file_desriptor:
                pickle.dump(old_list_of_files, file_desriptor)
        else:
            log.debug("no update of list of files necessary")

    def _scrub(self):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@gmx.de
        :Date: 2017-08-23 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
        """
        self._scrubbing = True
        self._semaphore_lock.acquire()
        if self._scrubbing:
            log = logging.getLogger(
                "pfu.simscrub."+threading.currentThread().name)
            file_handler = logging.handlers.WatchedFileHandler(
                os.path.join(self._config_dir, 'log'))  # not thread safe
            file_handler.setFormatter(
                logging.Formatter(
                    '%(asctime)s %(threadName)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'))
            file_handler.setLevel(self._loglevel)
            log.addHandler(file_handler)
            log.setLevel(self._loglevel)
            list_of_files = None
            with open(os.path.join(self._config_dir, 'list'),
                      'rb') as file_desriptor:
                list_of_files = pickle.load(file_desriptor)
            if self._update:
                self._do_update(log, list_of_files)
        if self._scrubbing:
            log.info("start scrubbing at %i/%i",
                     self._status,
                     len(list_of_files))
            time_offset = time.perf_counter()
            for i in range(self._status, len(list_of_files)):
                self._read_file(list_of_files[i], log)
                if (self._scrubbing and
                        (time.perf_counter()-time_offset > self._time_delta)):
                    self._write_status(i)
                    log.debug("status: %i/%i", i, len(list_of_files))
                    # give another one the chance:
                    self._semaphore_lock.release()
                    time.sleep(0.1)
                    self._semaphore_lock.acquire()
                    time_offset = time.perf_counter()
                if not self._scrubbing:
                    log.debug("break")
                    self._status = max(0, i-1)
                    break
            if self._scrubbing:
                self._status = 0
            self._write_status()
            if self._scrubbing:
                log.info("finished scrubbing at %i/%i",
                         self._status,
                         len(list_of_files))
            else:
                log.info("interrupted at %i/%i",
                         self._status,
                         len(list_of_files))
        self._scrubbing = False
        self._semaphore_lock.release()
        self._event_lock.set()

    def stop_scrubbing(self):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@gmx.de
        :Date: 2017-01-06 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
        """
        self._scrubbing = False
