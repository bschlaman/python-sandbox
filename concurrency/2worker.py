import asyncio
import random
from pprint import pprint
import time

random.seed(4)

delays = [2, 1, 4, 2, 5, 1]
rev_delays = list(reversed(delays))

def work(d):
    print("sleep for", d)
    # time.sleep(d)
    return d

async def worker(tasks_queue, results_queue):
    while True:
        task_id, task, args = await tasks_queue.get()
        await asyncio.sleep(random.random())
        result = task(args)
        await results_queue.put((task_id, result))

async def main_coroutine(tasks_queue, results_queue):
    task_results = {}
    for i in range(5):
        task_id = f"main_{i}"
        args = i
        await tasks_queue.put((task_id, work, args))
        task_results[task_id] = asyncio.create_task(results_queue.get())

    pprint({"main": task_results})

    for task_id, task_result in task_results.items():
        _, result = await task_result
        task_results[task_id] = result

    print(f"Main Coroutine Results: {task_results}")

async def secondary_coroutine(tasks_queue, results_queue):
    task_results = {}
    for i in range(5, 10):
        task_id = f"secondary_{i}"
        args = i
        await tasks_queue.put((task_id, work, args))
        task_results[task_id] = asyncio.create_task(results_queue.get())

    pprint({"secondary": task_results})

    for task_id, task_result in task_results.items():
        _, result = await task_result
        task_results[task_id] = result

    print(f"Secondary Coroutine Results: {task_results}")

async def run_parallel_coroutines():
    tasks_queue = asyncio.Queue()
    results_queue = asyncio.Queue()

    worker_task_1 = asyncio.create_task(worker(tasks_queue, results_queue))
    worker_task_2 = asyncio.create_task(worker(tasks_queue, results_queue))
    main_coroutine_task = asyncio.create_task(main_coroutine(tasks_queue, results_queue))
    secondary_coroutine_task = asyncio.create_task(secondary_coroutine(tasks_queue, results_queue))

    await asyncio.gather(main_coroutine_task, secondary_coroutine_task)
    worker_task_1.cancel()
    worker_task_2.cancel()

asyncio.run(run_parallel_coroutines())

