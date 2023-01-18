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
