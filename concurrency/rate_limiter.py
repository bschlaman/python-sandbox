"""
Key takeaways (ratelimiter):

1. While asyncio.Task is the highest level primitive, ef I want to delay the execution
   of the objects, I need to use coroutines.

2. It's important to note that in the below examples, there's only ever one event loop.

3. A nifty trick would be to add another callback to a Task if I wanted to aggregate
   results without using asyncio.gather

```python
    task.add_done_callback(self._aggregate_task_res)
    def _aggregate_task_res(self, task: asyncio.Task):
        self.results.append(task.result())
```

4. asyncio.Queue might be useful in context of multiple coroutines submitting jobs to
   a single RateLimiter instance
```python
def __init__(self, tasks):
    self.tasks: asyncio.Queue = asyncio.Queue()
    for task in tasks:
        self.tasks.put_nowait(task)
def start():
    while not self.tasks.empty():
        ...
```
"""
import asyncio
from enum import Enum
from typing import Coroutine, Iterable
import utils
import time


class RateLimitMode(Enum):
    BY_CONCURRENCY = "BY_CONCURRENCY"
    BY_RATE = "BY_RATE"


class RateLimiter:
    def __init__(self, coros: Iterable[Coroutine], mode: RateLimitMode):
        self._exec_func = {
            RateLimitMode.BY_CONCURRENCY: self._by_concurrency,
            RateLimitMode.BY_RATE: self._by_rate,
        }[mode]
        self.coros = coros

    async def begin_execution(self) -> list[dict]:
        return await self._exec_func()

    async def _by_concurrency(self):
        """Ratelimit based on number of concurrent executions"""
        sem = asyncio.Semaphore(2)
        tasks = []
        for coro in self.coros:
            await sem.acquire()
            task = asyncio.create_task(coro)
            task.add_done_callback(lambda _: sem.release())
            tasks.append(task)
        return await asyncio.gather(*tasks)

    async def _by_rate(self):
        """Ratelimit based on a fixed rate of tps"""
        delay = 1
        tasks = []
        for coro in self.coros:
            tasks.append(asyncio.create_task(coro))
            print("sleeping for 1")
            await asyncio.sleep(delay)
        return await asyncio.gather(*tasks)


delays = [2, 1, 4, 2, 5, 1]


async def main():
    print("creating tasks")
    coros = [utils.fetch_data_delayed_async(delay) for delay in delays]

    start_time = time.time()

    rl = RateLimiter(coros, RateLimitMode.BY_CONCURRENCY)
    # ...
    print(await rl.begin_execution())

    print(f"total time elapsed: {round(time.time() - start_time, 3)}")


if __name__ == "__main__":
    asyncio.run(main())
