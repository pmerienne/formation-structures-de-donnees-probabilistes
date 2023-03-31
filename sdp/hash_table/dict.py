from typing import TypeVar, Optional

K = TypeVar('K')
V = TypeVar('V')


class Dict:
    def get(self, key: K) -> Optional[V]:
        pass

    def set(self, key: K, value: V):
        pass


class PythonDict(Dict):
    def __init__(self):
        self.records: dict[K, V] = {}

    def get(self, key: K) -> Optional[V]:
        return self.records.get(key)

    def set(self, key: K, value: V):
        self.records[key] = value


class ListBasedDict(Dict):
    def __init__(self):
        self.records: list[(K, V)] = []

    def get(self, key: K) -> Optional[V]:
        for current_key, current_value in self.records:
            if current_key == key:
                return current_value
        return None

    def set(self, key: K, value: V):
        new_record = (key, value)
        for index, (current_key, current_value) in enumerate(self.records):
            if current_key == key:
                self.records[index] = new_record
                return
        self.records.append(new_record)


class DumbHashDict(Dict):
    def __init__(self, size: int = 10):
        self.size = size
        self.records: list[V] = [None] * size

    def get(self, key: K) -> Optional[V]:
        index = hash(key) % self.size
        return self.records[index]

    def set(self, key: K, value: V):
        index = hash(key) % self.size
        self.records[index] = value


class ChainedHashTable(Dict):
    def __init__(self, size: int = 10):
        self.size = size
        self.partitions: list[list[(K, V)]] = [[] for _ in range(self.size)]

    def get(self, key: K) -> Optional[V]:
        index = hash(key) % self.size
        partition = self.partitions[index]
        for current_key, current_value in partition:
            if current_key == key:
                return current_value
        return None

    def set(self, key: K, value: V):
        index = hash(key) % self.size
        partition = self.partitions[index]
        for index, (current_key, current_value) in enumerate(partition):
            if current_key == key:
                partition[index] = (key, value)
                return
        partition.append((key, value))
