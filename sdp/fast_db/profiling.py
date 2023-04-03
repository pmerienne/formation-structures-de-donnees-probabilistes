import cProfile
from pathlib import Path
from tempfile import TemporaryDirectory

from sdp.fast_db import FastDB
from sdp.fast_db.db import SuperFastDB, SuperDuperFastDB

nb_records = 10000


def fill_db(db: FastDB):
    for i in range(nb_records):
        key = str(i)
        value = i
        db.set(key, value)


def get_absents(db: FastDB):
    for i in range(nb_records, nb_records * 2):
        key = str(i)
        db.get(key)


if __name__ == '__main__':
    print('[FastDB] Get absent')
    with TemporaryDirectory() as temporary_directory:
        fast_db = FastDB(Path(temporary_directory))
        fill_db(fast_db)
        cProfile.run('get_absents(fast_db)')

    print('[SuperFastDB] Get absent')
    with TemporaryDirectory() as temporary_directory:
        super_fast_db = SuperFastDB(Path(temporary_directory), nb_records, 0.01)
        fill_db(super_fast_db)
        cProfile.run('get_absents(super_fast_db)')

    print('[SuperDuperFastDB] Get absent')
    with TemporaryDirectory() as temporary_directory:
        super_fast_db = SuperDuperFastDB(Path(temporary_directory))
        fill_db(super_fast_db)
        cProfile.run('get_absents(super_fast_db)')
