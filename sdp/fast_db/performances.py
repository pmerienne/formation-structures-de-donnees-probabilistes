import random
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4

from sdp.fast_db import FastDB, FastDBIndex, FastDBStorage, FastDBSerializer
from sdp.fast_db.bloom import BloomFilter
from sdp.fast_db.db import SuperFastDB, SuperDuperFastDB
from sdp.perf_utils import pretty_timeit
from tests.fast_db.model import User

keys = []


def clear():
    keys.clear()


def set_value(db: FastDB):
    key = str(uuid4())
    value = User()
    db.set(key, value)
    keys.append(key)


def get_absent_value(db: FastDB):
    key = str(uuid4())
    db.get(key)


def get_existing_value(db: FastDB):
    key = random.choice(keys)
    db.get(key)


def set_position(index: FastDBIndex):
    key = str(uuid4())
    position = random.randint(0, 10)
    index.set_position(key, position)
    keys.append(key)


def get_existing_position(index: FastDBIndex):
    key = random.choice(keys)
    index.get_position(key)


def get_absent_position(index: FastDBIndex):
    key = str(uuid4())
    index.get_position(key)


def write_value(storage: FastDBStorage):
    value = User()
    position = storage.write_value(value)
    keys.append(position)


def read_value(storage: FastDBStorage):
    position = random.choice(keys)
    storage.read_value(position)


def serialize_value(serializer: FastDBSerializer):
    raw = serializer.serialize(User())
    keys.append(raw)


def deserialize_value(serializer: FastDBSerializer):
    raw = random.choice(keys)
    serializer.deserialize(raw)


def bloom_add(bloom_filter: BloomFilter):
    key = str(uuid4())
    bloom_filter.add(key)


def bloom_contains(bloom_filter: BloomFilter):
    key = str(uuid4())
    bloom_filter.contains(key)


if __name__ == '__main__':
    print('# FastDB')
    with TemporaryDirectory() as temporary_directory:
        temporary_directory = Path(temporary_directory)
        db = FastDB(temporary_directory)
        pretty_timeit(lambda: set_value(db), prefix="set: ", loops=100)
        pretty_timeit(lambda: get_absent_value(db), prefix="get (absent): ", loops=100)
        pretty_timeit(lambda: get_existing_value(db), prefix="get (existing): ", loops=100)
        clear()

    print('# SuperFastDB')
    with TemporaryDirectory() as temporary_directory:
        temporary_directory = Path(temporary_directory)
        super_db = SuperFastDB(temporary_directory, 500, 0.01)
        pretty_timeit(lambda: set_value(super_db), prefix="set: ", loops=100)
        pretty_timeit(lambda: get_absent_value(super_db), prefix="get (absent): ", loops=100)
        pretty_timeit(lambda: get_existing_value(super_db), prefix="get (existing): ", loops=100)
        clear()

    print('# SuperDuperFastDB')
    with TemporaryDirectory() as temporary_directory:
        temporary_directory = Path(temporary_directory)
        super_duper_db = SuperDuperFastDB(temporary_directory)
        pretty_timeit(lambda: set_value(super_duper_db), prefix="set: ", loops=100)
        pretty_timeit(lambda: get_absent_value(super_duper_db), prefix="get (absent): ", loops=100)
        pretty_timeit(lambda: get_existing_value(super_duper_db), prefix="get (existing): ", loops=100)
        clear()

    print('# BloomFilter')
    with TemporaryDirectory() as temporary_directory:
        bloom_filter = BloomFilter(Path(temporary_directory) / str(uuid4()), 500, 0.01)
        pretty_timeit(lambda: bloom_add(bloom_filter), prefix="add: ", loops=100)
        pretty_timeit(lambda: bloom_contains(bloom_filter), prefix="contains: ", loops=100)
        clear()

    print('# FastDBIndex')
    with TemporaryDirectory() as temporary_directory:
        temporary_file = Path(temporary_directory) / str(uuid4())
        index = FastDBIndex(temporary_file)
        pretty_timeit(lambda: set_position(index), prefix="set_position: ", loops=100)
        pretty_timeit(lambda: get_absent_position(index), prefix="get_position (absent): ", loops=100)
        pretty_timeit(lambda: get_existing_position(index), prefix="get_position (existing): ", loops=100)
        clear()

    print('# FastDBStorage')
    with TemporaryDirectory() as temporary_directory:
        temporary_file = Path(temporary_directory) / str(uuid4())
        storage = FastDBStorage(temporary_file)
        pretty_timeit(lambda: write_value(storage), prefix="write: ", loops=100)
        pretty_timeit(lambda: read_value(storage), prefix="read: ", loops=100)
        clear()

    print('# FastDBSerializer')
    serializer = FastDBSerializer()
    pretty_timeit(lambda: serialize_value(serializer), prefix="serialize: ", loops=100)
    pretty_timeit(lambda: deserialize_value(serializer), prefix="deserialize: ", loops=100)

