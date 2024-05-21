#!/usr/bin/env python3
"""CLI to interact with caching system
"""

BaseCaching = __import__('base_caching').BaseCaching
LIFOCache = __import__('2-lifo_cache').LIFOCache
FIFOCache = __import__('1-fifo_cache').FIFOCache
LRUCache = __import__('3-lru_cache').LRUCache
MRUCache = __import__('4-mru_cache').MRUCache



class CachingCLI:
    def __init__(self, cache_systems):
        self.cache_systems = cache_systems
        self.current_cache = None

    def select_cache_system(self):
        print("Select a caching system:")
        for i, system in enumerate(self.cache_systems.keys(), start=1):
            print(f"{i}. {system}")
        choice = int(input("Enter your choice (number): ")) - 1
        cache_name = list(self.cache_systems.keys())[choice]
        self.current_cache = self.cache_systems[cache_name]

    def run(self):
        self.select_cache_system()
        while True:
            command = input("Enter command: ").split()
            if not command:
                continue
            cmd, *args = command

            if cmd == "put":
                if len(args) == 2:
                    self.current_cache.put(*args)
                else:
                    print("Invalid 'put' command. Usage: put <key> <value>")
            elif cmd == "get":
                if len(args) == 1:
                    print(self.current_cache.get(args[0]))
                else:
                    print("Invalid 'get' command. Usage: get <key>")
            elif cmd == "show":
                self.current_cache.print_cache()
            elif cmd == "switch":
                self.select_cache_system()
            elif cmd == "exit":
                break
            else:
                print("Unknown command.")

# Example cache system classes (BasicCache, FIFOCache, etc.) should be defined above

# Example usage
cache_systems = {
    "FIFOCache": FIFOCache(),
    "LIFOCache": LIFOCache(),
    "LRUCache": LRUCache(),
    "MRUCache": MRUCache(),
    # Add other caching systems here
}

if __name__ == "__main__":
    cli = CachingCLI(cache_systems)
    cli.run()
