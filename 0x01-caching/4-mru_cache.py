#!/usr/bin/env python3
"""A script for MRU caching system
"""


from collections import OrderedDict
BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    """mru cache system"""

    def __init__(self):
        super().__init__()
        self.stack = []

    def put(self, key, item):
        """ put key value pair into cache"""
        discarded = None
        if (key is None or item is None):
            return

        if key in self.cache_data:
            self.stack.remove(key)

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:

            discarded = self.stack.pop()
            del self.cache_data[discarded]
            # self.stack.remove(key)
            print(f"DISCARD: {discarded}")
        self.cache_data[key] = item
        self.stack.append(key)

    def get(self, key):
        """ return the value in self.cache_data linked to key.
        If key is None or if the key doesn’t exist
        in self.cache_data, return None."""
        if key is None or key not in self.cache_data:
            return None
        self.stack.remove(key)
        self.stack.append(key)
        return self.cache_data[key]
