import mmh3


class BloomFilter:

    def __init__(self, hash_number, table_size):
        self.hash_number = hash_number
        self.table_size = table_size
        self.table = [0] * table_size

    def add_item(self, item):
        for i in range(0, self.hash_number):
            hash_index = mmh3.hash(item, i) % self.table_size
            self.table[hash_index] = 1

    def exists(self, item) -> bool:
        for i in range(0, self.hash_number):
            hash_index = mmh3.hash(item, i) % self.table_size
            if self.table[hash_index] == 0:
                return False
        return True