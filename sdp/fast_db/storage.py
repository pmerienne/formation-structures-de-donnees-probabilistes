import os
import pickle
import sys
from pathlib import Path
from typing import Any

INT_SIZE = 4


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
