from pathlib import Path
from typing import Any, Optional

from sdp.fast_db.bloom import BloomFilter
from sdp.fast_db.index import FastDBIndex
from sdp.fast_db.storage import FastDBStorage

INT_SIZE = 4


class FastDB:
    def __init__(self, root_directory: Path):
        self.root_directory = root_directory
        self.storage = FastDBStorage(root_directory / 'data.db')
        self.index = FastDBIndex(root_directory / 'index.db')
        self.bloom = BloomFilter(6, 9585)

    def get(self, key: str) -> Optional[Any]:
        if not self.bloom.exists(key):
            return None
        position = self.index.get_position(key)
        return self.storage.read_value(position) if position is not None else None

    def set(self, key: str, value: Any):
        position = self.storage.write_value(value)
        self.index.set_position(key, position)
        self.bloom.add_item(key)

    def close(self):
        self.index.close()
        self.storage.close()
