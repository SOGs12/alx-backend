#!/usr/bin/env python3
"""A script for caching system
"""


BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """inherits from BaseCaching

    Args:
        BaseCaching (_type_): _description_
    """
    def __init__(self):
        """initialize BasicCache"""
        super().__init__()

    def put(self, key, item):
        """assign to the dictionary
        self.cache_data the item value for the key key
        """
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """ return the value in self.cache_data linked to key

        Args:
            key (_type_): _description_
        """
        if key not in self.cache_data or key is None:
            return None
        return self.cache_data.get(key)
