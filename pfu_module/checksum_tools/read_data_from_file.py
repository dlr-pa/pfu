"""
Author: Daniel Mohr.

Date: 2016-12-03 (last change).

License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""


def read_data_from_file(buf_size, data_file, size, hash_objects):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2016-12-04 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

    Read size Bytes from the file data_file in chunks and update
    hash objects with these data chunks.

    :param buf_size: read this amount of Bytes at once
    :param data_file: file object from where to read
    :param size: amount of Bytes to read
    :param hash_objects: list of hash objects to update by the data
    """
    data_read = 0
    while data_read < size:
        number_of_bytes = min(buf_size, size-data_read)
        buf = data_file.read(number_of_bytes)
        if len(buf) == 0:
            break
        data_read += len(buf)
        for hash_object in hash_objects:
            hash_object.update(buf)
