#!/usr/bin/env python3
"""A script for LIFO caching system
"""


from collections import deque
BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """LIFO cache system"""

    def __init__(self):
        super().__init__()
        self.order = deque()

    def put(self, key, item):
        """ put key value pair into cache"""
        if (key is None or item is None):
            return
        capacity = BaseCaching.MAX_ITEMS
        self.cache_data[key] = item
        self.order.append(key)
        # if key in self.cache_data:
        #     self.cache_data[key] = item
        if len(self.cache_data) > capacity:
            key_to_pop = self.order[-2]
            del self.cache_data[key_to_pop]
            print(f"DISCARD: {key_to_pop}")

    def get(self, key):
        """ return the value in self.cache_data linked to key.
        If key is None or if the key doesn’t exist
        in self.cache_data, return None."""
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data.get(key)
