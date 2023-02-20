import asyncio
from utils import fetch_data_delayed_async_pprint, get_coro_name

delays = [2, 1, 4, 2, 5, 1]
rev_delays = list(reversed(delays))


task_queue = asyncio.Queue()


async def worker():
    print(f"worker started on coro: {get_coro_name()}")
    while True:
        task_id, task, stop_event = await task_queue.get()
        # result = await asyncio.create_task(task)
        result = await task
        stop_event.set()
        print(f"[worker]: task: {task_id} result: {result['delay']}\n")


async def main_coroutine():
    print(f"main coro started on coro: {get_coro_name()}")
    # tasks = [asyncio.sleep(d, result=d) for d in delays]
    # tasks = [fetch_data_delayed_async_pprint(d) for d in delays]
    tasks = {fetch_data_delayed_async_pprint(d): asyncio.Event() for d in delays}
    for task_id, task in enumerate(tasks):
        await task_queue.put(
            (
                task_id,
                task,
                tasks[task],
            )
        )
        print(f"put task: {task_id}")

    for event in tasks.values():
        await event.wait()

    # await asyncio.gather(*tasks)


async def main():
    print(f"main started on coro: {get_coro_name()}")
    worker_task = asyncio.create_task(worker())
    main_task = asyncio.create_task(main_coroutine())
    await asyncio.gather(main_task)
    # await task_queue.put((None, None, None))
    worker_task.cancel()


asyncio.run(main())
