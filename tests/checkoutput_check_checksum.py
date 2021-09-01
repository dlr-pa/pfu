"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-05-17
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import re


def checkoutput(out):
    out = out.decode()
    ok = True
    regexp_without_hash = re.compile(r'data file without hash: ([0-9]+)')
    regexp_without_data = re.compile(r'hash without data file: ([0-9]+)')
    regexp_matching_hash = re.compile(
        r'data file with matching hash\(es\): ([0-9]+)')
    regexp_not_matching_hash = re.compile(
        r'data file with not matching hash\(es\): ([0-9]+)')
    for line in out.split('\n'):
        without_hash = regexp_without_hash.findall(line)
        if without_hash and (int(without_hash[0]) != 0):
            ok = False
            break
        without_data = regexp_without_data.findall(line)
        if without_data and (int(without_data[0]) != 0):
            ok = False
            break
        matching_hash = regexp_matching_hash.findall(line)
        if matching_hash and (int(matching_hash[0]) == 0):
            ok = False
            break
        not_matching_hash = regexp_not_matching_hash.findall(line)
        if not_matching_hash and (int(not_matching_hash[0]) != 0):
            ok = False
            break
    return ok
