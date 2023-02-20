# Brendan's Python Sandbox

Welcome!

## Introduction

Messing around with Python and some libraries. All code herein is nonsense test code; don't read into it too much.

Something something life-long-learner...

### Module: Concurrency

Exploration and comparison of strategies to cleanly achieve concurrency in python for I/O bound tasks.

**Conclusion**

My current thoughts about python I/O task concurrent computing can be sumarized by the following analogy.

`multiprocessing:multithreading::multithreading:asyncio`

These libraries are not technically analogous, as they use 3 entirely different mechanisms to speed up I/O, but my claim is about complexity. Essentially, always prefer the highest level abstraction possible, which means asyncio for I/O tasks.

Within `asyncio`, `asyncio.gather` should be used unless jobs might be submitted from multiple coroutines. The primary use case for `asyncio.Queue` is in a pub/sub context (multiple producers and consumers) to limit the rate of work being done or account for differences in processing time between the consumers and producers. I don't see a reason to use it in the context of a single producer and multiple consumers.

Additionally, I don't think there's a good way to use `asyncio.as_completed` if I care about matching the results to the inputs, as I don't know of a way to extract the original coro from `as_completed`.

#### Worker-Queue concurrency pattern

Goals for this pattern:

- worker coroutine schedules tasks and does the work either in its own coroutine or in a child coroutine
  - multiple workers: `await task`
  - single worker: `await asyncio.create_task(task)`
- multiple coroutines can submit tasks to a single queue
- the submitter coroutine knows when all tasks are complete and can match results to the input tasks

This pattern would probably be overkill if I weren't implementing a Ratelimiter, since any coroutine calling `asyncio.create_task` will schedule a task to be completed on the event loop.

I figure that allowing the worker nodes to enforce ratelimits will allow the submitter coroutines to be none the wiser that this is an async application. In other words, a submitter simply waits in line and proceeds when they have their results.
