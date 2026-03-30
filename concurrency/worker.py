import asyncio
import random

from utils import fetch_data_delayed_async_pprint

random.seed(4)

async def worker(tasks_queue, results_queue):
    while True:
        task_id, task = await tasks_queue.get()
        result = task()
        await results_queue.put((task_id, result))

async def main_coroutine(tasks_queue, results_queue):
    task_results = {}
    for task_id in [1,4,2,3]:
        task = fetch_data_delayed_async_pprint(task_id)
        await tasks_queue.put((task_id, task))
        task_results[task_id] = asyncio.create_task(results_queue.get())

    for task_id, task_result in task_results.items():
        _, result = await task_result
        task_results[task_id] = result

    print(task_results)

async def run_parallel_coroutines():
    tasks_queue = asyncio.Queue()
    results_queue = asyncio.Queue()

    worker_task = asyncio.create_task(worker(tasks_queue, results_queue))
    main_coroutine_task = asyncio.create_task(main_coroutine(tasks_queue, results_queue))

    await asyncio.gather(worker_task, main_coroutine_task)

asyncio.run(run_parallel_coroutines())

