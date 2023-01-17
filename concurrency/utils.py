import concurrent.futures
import requests
import time
import aiohttp


async def fetch_data_delayed_async(delay_seconds: int):
    url = "http://pi4:8081/api/echodelay?t={t}"
    async with aiohttp.ClientSession() as client:
        async with client.get(url.format(t=delay_seconds)) as res:
            return await res.json()


def fetch_data_delayed(delay_seconds: int):
    url = "http://pi4:8081/api/echodelay?t={t}"
    res = requests.get(url.format(t=delay_seconds))
    return res.json()


def handle_future(f: concurrent.futures.Future, start_time: float):
    res = f.result()
    print(
        round(time.time() - start_time, 3),
        res.get("delay"),
        res.get("user_agent"),
    )


def handle_future_no_timing(f: concurrent.futures.Future):
    res = f.result()
    print(
        res.get("delay"),
        res.get("user_agent"),
    )
