"""
Key takeaways (ThreadPoolExecutor job submission example):

1. the best way to obtain true concurrency is to use `add_done_callback`
"""
import concurrent.futures
import time

import utils

executor = None


def init_executor():
    global executor
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    return executor


def get_executor_instance() -> concurrent.futures.ThreadPoolExecutor:
    if not isinstance(executor, concurrent.futures.ThreadPoolExecutor):
        raise Exception
    return executor


def submit_job(executor: concurrent.futures.ThreadPoolExecutor, t: int):
    print(f"calling submit_job: {t}")
    future = executor.submit(utils.fetch_data_delayed, t)
    future.add_done_callback(utils.handle_future_no_timing)


def submit_jobs(executor: concurrent.futures.ThreadPoolExecutor):
    futures = [executor.submit(utils.fetch_data_delayed, t) for t in range(5, 1, -1)]

    start_time = time.time()

    submit_job(executor, 1)
    submit_job(executor, 2)
    submit_job(executor, 4)
    submit_job(executor, 1)
    submit_job(executor, 8)

    print("jobs submitted")

    for f in concurrent.futures.as_completed(futures):
        utils.handle_future(f, start_time)

    print(f"total time elapsed: {round(time.time() - start_time, 3)}")


def main():
    e = init_executor()
    submit_jobs(e)
    e.shutdown()


if __name__ == "__main__":
    main()
