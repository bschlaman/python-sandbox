"""
Key takeaways (asyncio job submission example):

1. Event loops use cooperative scheduling; an event loop runs one Task at a time.
   The event loop is freed only when a Task awaits a Future.

2. I probably cant use `requests` traditionally here.
   Instead, I use `aiohttp` to make get requests in a coroutine
   Another option would be to use `asyncio.gather`

3. `asyncio.gather` is the way to go when working with `asyncio`
   (as opposed to `asyncio.create_task`), namely because I can gather
   results.
"""
import time
import asyncio
import utils

delays = [2, 1, 4, 2, 5, 1]


async def worker(name: str, queue: asyncio.Queue):
    while True:
        await asyncio.sleep(0.2)
        task = await queue.get()
        seconds = task["seconds"]
        print(f"{name} picked up task: {task['seconds']}")

        res = await utils.fetch_data_delayed_async(seconds)

        queue.task_done()
        print(f"{name} processed task: {seconds} (res: {res.get('delay')})")


async def main_create_task():
    queue = asyncio.Queue()
    print("putting tasks")
    for delay in delays:
        queue.put_nowait({"seconds": delay})
    print(f"putting tasks (done) ({queue.qsize()} items)\n")

    print("creating workers")
    tasks = []
    for i in range(3):
        task = asyncio.create_task(worker(f"worker-{i}", queue))
        tasks.append(task)
    print("creating workers (done)\n")

    start_time = time.time()
    await queue.join()

    print(f"total time elapsed: {round(time.time() - start_time, 3)}")

    # Cancel our worker tasks.
    for task in tasks:
        task.cancel()
    # Wait until all worker tasks are cancelled.
    await asyncio.gather(*tasks, return_exceptions=True)


async def main_gather():
    coros = [utils.fetch_data_delayed_async(delay) for delay in delays]
    start_time = time.time()
    results = await asyncio.gather(*coros)
    for coro, res in zip(coros, results):
        print(coro, res.get("delay"))

    print(f"total time elapsed: {round(time.time() - start_time, 3)}")


if __name__ == "__main__":
    asyncio.run(main_gather())
