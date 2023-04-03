import math
import os
import sys
from pathlib import Path
from typing import Optional

import mmh3
from bitarray import bitarray


INT_SIZE = 8


class BloomFilter:
    def __init__(self, path: Path, expected_records: int, expected_fp: float):
        self.path = path
        self.path.touch()
        self.file = open(path, 'rb+')

        if os.fstat(self.file.fileno()).st_size == 0:
            self.bit_array_size = -(expected_records * math.log(expected_fp)) / (math.log(2) ** 2)
            self.bit_array_size = int(self.bit_array_size)
            self.hash_count = (self.bit_array_size / expected_records) * math.log(2)
            self.hash_count = int(self.hash_count)

            self.bit_array = bitarray(self.bit_array_size)
            self.bit_array.setall(0)
            self._init_file()
        else:
            self._load()

    def add(self, value: str):
        for i in range(self.hash_count):
            digest = mmh3.hash(value, i) % self.bit_array_size
            self.bit_array[digest] = True
        self._dump()

    def contains(self, value: str):
        for i in range(self.hash_count):
            digest = mmh3.hash(value, i) % self.bit_array_size
            if not self.bit_array[digest]:
                return False
        return True

    def close(self):
        self.file.close()

    def _init_file(self):
        self.file.seek(0)
        self.file.write(self.bit_array_size.to_bytes(INT_SIZE, byteorder=sys.byteorder))
        self.file.write(self.hash_count.to_bytes(INT_SIZE, byteorder=sys.byteorder))
        self.file.write(self.bit_array.tobytes())

    def _dump(self):
        self.file.seek(INT_SIZE + INT_SIZE)
        self.file.write(self.bit_array.tobytes())

    def _load(self):
        self.bit_array_size = int.from_bytes(self.file.read(INT_SIZE), byteorder=sys.byteorder)
        self.hash_count = int.from_bytes(self.file.read(INT_SIZE), byteorder=sys.byteorder)
        self.bit_array = bitarray()
        self.bit_array.fromfile(self.file)



