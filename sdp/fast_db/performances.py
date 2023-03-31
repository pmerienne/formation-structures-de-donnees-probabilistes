import random
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4

from sdp.fast_db import FastDB, FastDBIndex, FastDBStorage, FastDBSerializer
from sdp.perf_utils import pretty_timeit
from tests.fast_db.model import User

keys = []
positions = []
serialized = []


def set_value(db: FastDB):
    key = str(uuid4())
    value = User()
    db.set(key, value)
    keys.append(key)


def get_random_value(db: FastDB):
    existing_key = random.random() > 0.5
    key = random.choice(keys) if existing_key else str(uuid4())
    db.get(key)


def set_position(index: FastDBIndex):
    key = str(uuid4())
    position = random.randint(0, 10)
    index.set_position(key, position)
    keys.append(key)


def get_random_position(index: FastDBIndex):
    existing_key = random.random() > 0.5
    key = random.choice(keys) if existing_key else str(uuid4())
    index.get_position(key)


def write_value(storage: FastDBStorage):
    value = User()
    position = storage.write_value(value)
    positions.append(position)


def read_value(storage: FastDBStorage):
    position = random.choice(positions)
    storage.read_value(position)


def serialize_value(serializer: FastDBSerializer):
    raw = serializer.serialize(User())
    serialized.append(raw)


def deserialize_value(serializer: FastDBSerializer):
    raw = random.choice(serialized)
    serializer.deserialize(raw)


if __name__ == '__main__':
    print('# FastDB')
    with TemporaryDirectory() as temporary_directory:
        temporary_directory = Path(temporary_directory)
        db = FastDB(temporary_directory)
        pretty_timeit(lambda: set_value(db), prefix="set: ", loops=100)
        pretty_timeit(lambda: get_random_value(db), prefix="get: ", loops=100)

    print('# FastDBIndex')
    with TemporaryDirectory() as temporary_directory:
        temporary_file = Path(temporary_directory) / str(uuid4())
        index = FastDBIndex(temporary_file)
        pretty_timeit(lambda: set_position(index), prefix="set_position: ", loops=100)
        pretty_timeit(lambda: get_random_position(index), prefix="get_position: ", loops=100)

    print('# FastDBStorage')
    with TemporaryDirectory() as temporary_directory:
        temporary_file = Path(temporary_directory) / str(uuid4())
        storage = FastDBStorage(temporary_file)
        pretty_timeit(lambda: write_value(storage), prefix="write: ", loops=100)
        pretty_timeit(lambda: read_value(storage), prefix="read: ", loops=100)

    print('# FastDBSerializer')
    serializer = FastDBSerializer()
    pretty_timeit(lambda: serialize_value(serializer), prefix="serialize: ", loops=100)
    pretty_timeit(lambda: deserialize_value(serializer), prefix="deserialize: ", loops=100)
