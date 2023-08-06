"""
    pyexcel.utils
    ~~~~~~~~~~~~~~~~~~~

    Utility functions for pyexcel

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
from .sheets import Sheet
import sys
if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict


def to_array(o):
    """convert a reader iterator to an array"""
    array = []
    for i in o:
        array.append(i)
    return array


def to_dict(o):
    """convert a reader iterator to a dictionary"""
    the_dict = OrderedDict()
    series = "Series_%d"
    count = 1
    for c in o:
        if type(c) == dict:
            the_dict.update(c)
        elif isinstance(c, Sheet):
            the_dict.update({c.name: to_array(c)})
        else:
            key = series % count
            the_dict.update({key: c})
            count += 1
    return the_dict


def to_records(reader, custom_headers=None):
    """
    Make an array of dictionaries

    It takes the first row as keys and the rest of
    the rows as values. Then zips keys and row values
    per each row. This is particularly helpful for
    database operations.
    """
    if isinstance(reader, Sheet) is False:
        raise NotImplementedError
    need_revert = False
    headers = reader.series()
    if len(headers) == 0:
        # this means the reader is not a series
        # reader
        reader.become_series()
        headers = reader.series()
        need_revert = True
    if custom_headers:
        headers = custom_headers
    ret = []
    for row in reader.rows():
        the_dict = dict(zip(headers, row))
        ret.append(the_dict)

    if need_revert:
        reader.become_sheet()
    return ret


def to_one_dimensional_array(iterator):
    """convert a reader to one dimensional array"""
    array = []
    for i in iterator:
        if type(i) == list:
            array += i
        else:
            array.append(i)
    return array
