#!/usr/bin/env python3
"""A script for LRU caching system
"""


from collections import OrderedDict
BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """LIFO cache system"""

    def __init__(self):
        super().__init__()
        self.order = OrderedDict()

    def put(self, key, item):
        """ put key value pair into cache"""
        discarded = None
        if (key is None or item is None):
            return
        self.cache_data[key] = item
        self.order[key] = item
        self.order.move_to_end(key)
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            discarded, item = self.order.popitem(last=False)
            del self.cache_data[discarded]
            print(f"DISCARD: {discarded}")

    def get(self, key):
        """ return the value in self.cache_data linked to key.
        If key is None or if the key doesn’t exist
        in self.cache_data, return None."""
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data.get(key)
