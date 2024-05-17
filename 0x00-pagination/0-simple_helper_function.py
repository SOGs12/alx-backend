#!/usr/bin/env python3
""" A script to generate a list for
particular pagination parameters"""


def index_range(page, page_size):
    """Return a tuple of size two
    containing a start index and an end index

    Args:
        page (INT): corresponding to the range of indexes
        page_size (INT): corresponding to the range of indexes
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return (start_index, end_index)
