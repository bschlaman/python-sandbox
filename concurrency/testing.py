import asyncio
import time

from utils import fetch_data_delayed_pprint, fetch_data_delayed_async_pprint

async def main():
    fetch_data_delayed_pprint(1)
    # await fetch_data_delayed_async(2)
    await asyncio.create_task(fetch_data_delayed_async_pprint(2))
    print("done")

asyncio.run(main())
