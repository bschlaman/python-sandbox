"""
Key takeaways (`iter(futures)` vs `as_completed(futures)`):

1. when delays are monotonically increasing, there is no difference
   between iterating over `futures` and iterating over `as_completed(futures)`

2. the overall execution time of the iteration also does not depend on
   the iterator

3. only when slower jobs happen to be submitted before faster jobs does
   the difference reveal itself: faster jobs can be processeses while
   slower jobs complete when using the `as_completed` iterator
"""
import concurrent.futures
import time

from . import utils


AS_COMPLETED_MODE = False

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    print("BEGIN TPE contextmgr")
    # futures = [executor.submit(fetch_data_delayed, t) for t in range(2, 6)]
    futures = [executor.submit(utils.fetch_data_delayed, t) for t in range(5, 1, -1)]
    print("jobs submitted")

    start_time = time.time()

    if AS_COMPLETED_MODE:
        for f in concurrent.futures.as_completed(futures):
            utils.handle_future(f, start_time)
    else:
        for f in futures:
            utils.handle_future(f, start_time)

    print(f"total time elapsed: {round(time.time() - start_time, 3)}")
