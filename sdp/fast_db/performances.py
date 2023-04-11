import math
from pathlib import Path
from random import randint
from tempfile import TemporaryDirectory

from sdp.fast_db import FastDB
from sdp.perf_utils import pretty_timeit


if __name__ == '__main__':

    expected_records = 1000
    expected_fp = 0.01
    bit_array_size = -(expected_records * math.log(expected_fp)) / (math.log(2) ** 2)
    bit_array_size = int(bit_array_size)

    hash_count = (bit_array_size / expected_records) * math.log(2)
    hash_count = int(hash_count)

    print(f'bit_array_size: {bit_array_size}, hash_count: {hash_count}')

    with TemporaryDirectory() as temporary_directory:
        fast_db = FastDB(Path(temporary_directory))
        # Fill db
        for i in range(1000):
            fast_db.set(str(i), i)

        # Mesurer les performances
        pretty_timeit(lambda: fast_db.get(str(randint(0, 1000))))
        #  Before: 0.02669884959977935 ± 0.0011658760761059845 per loop (mean ± std. dev. of 5 runs, 1000 loops each)
        #  After: 0.03131070139934309 ± 0.004349833321048779 per loop (mean ± std. dev. of 5 runs, 1000 loops each)
        pretty_timeit(lambda: fast_db.get(str(randint(1000, 10000))))
        #  Before: 0.021751707399380392 ± 0.00037901496457918893 per loop (mean ± std. dev. of 5 runs, 1000 loops each)
        #  After: 0.001821188401663676 ± 0.00012558176828088316 per loop (mean ± std. dev. of 5 runs, 1000 loops each)
        # pretty_timeit(lambda: str(randint(0, 1000)))
        #  0.0007925696008896921 ± 0.0001267092189044182 per loop (mean ± std. dev. of 5 runs, 1000 loops each)
