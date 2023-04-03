from pathlib import Path
from typing import Any, Optional

from sdp.fast_db.bloom import BloomFilter
from sdp.fast_db.index import FastDBIndex, ShelfIndex
from sdp.fast_db.storage import FastDBStorage

INT_SIZE = 4


class FastDB:
    def __init__(self, root_directory: Path):
        self.root_directory = root_directory
        self.storage = FastDBStorage(root_directory / 'data.db')
        self.index = FastDBIndex(root_directory / 'index.db')

    def get(self, key: str) -> Optional[Any]:
        position = self.index.get_position(key)
        return self.storage.read_value(position) if position is not None else None

    def set(self, key: str, value: Any):
        position = self.storage.write_value(value)
        self.index.set_position(key, position)

    def close(self):
        self.index.close()
        self.storage.close()


class SuperFastDB(FastDB):
    def __init__(self, root_directory: Path, bloom_filter_records: int = 100, bloom_filter_fp: float = 0.01):
        super().__init__(root_directory)
        self.bloom_filter = BloomFilter(root_directory / 'bloom.db', bloom_filter_records, bloom_filter_fp)

    def get(self, key: str) -> Optional[Any]:
        if self.bloom_filter.contains(key):
            return super().get(key)
        else:
            return None

    def set(self, key: str, value: Any):
        super().set(key, value)
        self.bloom_filter.add(key)

    def close(self):
        super().close()
        self.bloom_filter.close()


class SuperDuperFastDB(FastDB):
    def __init__(self, root_directory: Path):
        self.root_directory = root_directory
        self.storage = FastDBStorage(root_directory / 'data.db')
        self.index = ShelfIndex(root_directory / 'index.db')
