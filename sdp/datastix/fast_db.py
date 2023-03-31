import os
import pickle
import shelve
import sys
from pathlib import Path
from typing import Any, Optional


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


class FastDBIndex:  # TODO: use B+tree ?
    def __init__(self, index_path: Path):
        self.index_path = index_path
        self.index_file = shelve.open(str(index_path.absolute()))

    def get_position(self, key: str) -> Optional[int]:
        return self.index_file.get(key)

    def set_position(self, key: str, position: int):
        self.index_file[key] = position

    def close(self):
        self.index_file.close()


class FastDBStorage:
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.storage_file = open(storage_path, 'ab+')
        self.serializer = FastDBSerializer()

    def read_value(self, position: int) -> Any:
        self.storage_file.seek(position)
        value_size = int.from_bytes(self.storage_file.read(INT_SIZE), byteorder=sys.byteorder)
        raw_value = self.storage_file.read(value_size)
        value = self.serializer.deserialize(raw_value)
        return value

    def write_value(self, value: Any) -> int:
        raw_value = self.serializer.serialize(value)
        value_size = len(raw_value)

        self.storage_file.seek(0, os.SEEK_END)
        position = self.storage_file.tell()

        self.storage_file.write(value_size.to_bytes(INT_SIZE, byteorder=sys.byteorder))
        self.storage_file.write(raw_value)
        self.storage_file.flush()

        return position

    def close(self):
        self.storage_file.close()


class FastDBSerializer:
    def serialize(self, value: Any) -> bytes:
        return pickle.dumps(value)

    def deserialize(self, raw: bytes) -> Any:
        return pickle.loads(raw)
