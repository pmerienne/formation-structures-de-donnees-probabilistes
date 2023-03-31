import math
import timeit

from pydantic.main import BaseModel


def pretty_timeit(stmt, repeat=5, loops=1000, prefix=''):
    timer = timeit.Timer(stmt)
    raw_timings = timer.repeat(repeat, loops)
    timings = [1000.0 * dt / loops for dt in raw_timings]
    mean = math.fsum(timings) / len(timings)
    stddev = (math.fsum([(x - mean) ** 2 for x in timings]) / len(timings)) ** 0.5
    print(f"{prefix} {mean} ± {stddev} per loop (mean ± std. dev. of {repeat} runs, {loops} loops each)")
    worst = max(timings)
    best = min(timings)
    return PerformanceReport(repeat=repeat, loops=loops, mean=mean, stddev=stddev, worst=worst, best=best)


class PerformanceReport(BaseModel):
    repeat: int
    loops: int
    mean: float
    stddev: float
    worst: float
    best: float
