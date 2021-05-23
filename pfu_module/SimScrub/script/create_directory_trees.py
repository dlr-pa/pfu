"""
:Author: Daniel Mohr
:Email: daniel.mohr@gmx.de
:Date: 2017-01-29, 2021-05-23 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import base64
import hashlib
import os
import os.path
import pickle

import pfu_module.SimScrub


def create_directory_trees(args, log):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@gmx.de
    :Date: 2017-01-29, 2021-05-23 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
    """
    log.debug("directory trees: %s" % args.dir)
    for reldir in args.dir:
        absdir = os.path.abspath(reldir)
        absdir_hash = hashlib.sha512()
        absdir_hash.update(absdir.encode())
        absdir_hash = base64.b32encode(absdir_hash.digest())[:-2].lower()
        log.info(" directory tree: %s" % reldir)
        config_dir = os.path.join(args.config_data_directory[0],
                                  absdir_hash.decode())
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        log.info(" configs: %s" % config_dir)
        with open(os.path.join(config_dir, 'dir'), 'wb') as file_desriptor:
            pickle.dump(reldir, file_desriptor)
        list_of_files = pfu_module.SimScrub.create_file_list(reldir, log)
        with open(os.path.join(config_dir, 'list'), 'wb') as file_desriptor:
            pickle.dump(list_of_files, file_desriptor)
        with open(os.path.join(config_dir, 'status'), 'wb') as file_desriptor:
            pickle.dump(0, file_desriptor)
        with open(os.path.join(config_dir, 'log'), 'w') as file_desriptor:
            pass
