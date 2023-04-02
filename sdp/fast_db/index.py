import shelve
from pathlib import Path
from typing import Optional


class FastDBIndex:
    def __init__(self, index_path: Path):
        self.index_path = index_path
        self.index_file = shelve.open(str(index_path.absolute()))

    def get_position(self, key: str) -> Optional[int]:
        return self.index_file.get(key)

    def set_position(self, key: str, position: int):
        self.index_file[key] = position

    def close(self):
        self.index_file.close()
