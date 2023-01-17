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
