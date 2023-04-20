#!/usr/bin/env python3

from typing import Tuple
"""
Simple helper function
Returns two sizes i.e start and end index
"""


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Index_range - range of indexes concerning pagination parameter
    args:
        page(int): page num to return (pages are 1-indexed)
        page_size(int): num of items per page
    Return: tuple of range of indexes
    """
    start, end = 0, 0
    for i in range(page):
        start = end
        end += page_size

    return (start, end)
