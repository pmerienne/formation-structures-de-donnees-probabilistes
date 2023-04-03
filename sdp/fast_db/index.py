import shelve
import sys
from pathlib import Path
from typing import Optional

from bplustree import BPlusTree
from bplustree.serializer import StrSerializer


class FastDBIndex:
    def __init__(self, index_path: Path):
        self.index_path = index_path
        self.tree = BPlusTree(
            str(index_path),
            order=50,
            key_size=256, value_size=8, page_size=4096 * 16,
            serializer=StrSerializer()
        )

    def get_position(self, key: str) -> Optional[int]:
        serialized = self.tree.get(key)
        return int.from_bytes(serialized, byteorder=sys.byteorder) if serialized else None

    def set_position(self, key: str, position: int):
        serialized = position.to_bytes(8, byteorder=sys.byteorder)
        self.tree[key] = serialized

    def close(self):
        self.tree.close()


class ShelfIndex:
    def __init__(self, index_path: Path):
        self.index_path = index_path
        self.shelf = shelve.open(str(index_path.absolute()))

    def get_position(self, key: str) -> Optional[int]:
        return self.shelf.get(key)

    def set_position(self, key: str, position: int):
        self.shelf[key] = position

    def close(self):
        self.shelf.close()

