#!/usr/bin/env python3
"""Hypermedia pagination generating script
    """


import requests
import csv
import math
from typing import List


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


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Return the appropriate page of the dataset
        (i.e. the correct list of rows).

        Args:
            page (int, optional): Defaults to 1.
            page_size (int, optional): Defaults to 10.

        Returns:
            List[List]: _description_
        """
        dataset = self.dataset()

        assert isinstance(page, int)
        assert isinstance(page_size, int)

        assert page > 0
        assert page_size > 0
        try:
            indexing = index_range(page, page_size)
            return dataset[indexing[0]:indexing[1]]
        except IndexException as e:
            return []

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """returns a dictionary of hypermedia keys and values

        Args:
            page (int, optional):Defaults to 1.
            page_size (int, optional):Defaults to 10.
        """
        data = self.get_page(page, page_size)
        total_pages = len(self.dataset()) // page_size

        dict = {
            "page_size": page_size if page_size <= len(data) else len(data),
            "page": page,
            "data": data,
            "next_page": page + 1 if page >= 0 else None,
            "prev_page": page - 1 if page >= 1 else None,
            "total_pages": total_pages
            }
        return dict
