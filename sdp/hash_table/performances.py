from uuid import uuid4

from sdp.hash_table.dict import ListBasedDict, Dict, PythonDict, ChainedHashTable
from sdp.perf_utils import pretty_timeit


def create_record(some_dict: Dict):
    key = uuid4()
    value = uuid4()
    some_dict.set(key, value)


def get_record(some_dict: Dict):
    key = uuid4()
    return some_dict.get(key)


if __name__ == '__main__':
    my_dict = ListBasedDict()
    pretty_timeit(lambda: create_record(my_dict), prefix="ListBasedDict (set): ")
    pretty_timeit(lambda: get_record(my_dict), prefix="ListBasedDict (get): ")

    chained_dict_100 = ChainedHashTable(100)
    pretty_timeit(lambda: create_record(chained_dict_100), prefix="ChainedHashTable(100) (set): ")
    pretty_timeit(lambda: get_record(chained_dict_100), prefix="ChainedHashTable(100) (get): ")

    chained_dict_5k = ChainedHashTable(5000)
    pretty_timeit(lambda: create_record(chained_dict_5k), prefix="ChainedHashTable(5000) (set): ")
    pretty_timeit(lambda: get_record(chained_dict_5k), prefix="ChainedHashTable(5000) (get): ")

    python_dict = PythonDict()
    pretty_timeit(lambda: create_record(python_dict), prefix="PythonDict (set): ")
    pretty_timeit(lambda: get_record(python_dict), prefix="PythonDict (get): ")

