import asyncio
import concurrent.futures
import time

import aiohttp
import requests
import os
from colorama import Fore


def get_coro_name():
    return asyncio.current_task().get_coro().__name__


ENDPOINT = "home:8080"


async def fetch_data_delayed_async_pprint(delay_seconds: int):
    print(f"[...work: {delay_seconds}] coro: {get_coro_name()}")
    url = "http://{endpoint}/api/echodelay?t={t}"
    async with aiohttp.ClientSession() as client:
        async with client.get(url.format(endpoint=ENDPOINT, t=delay_seconds)) as res:
            rj = await res.json()
            print(f"{blu('delay')}: {rj['delay']}")
            return rj


async def fetch_data_delayed_async(delay_seconds: int):
    print(f"[...work: {delay_seconds}]")
    url = "http://{endpoint}/api/echodelay?t={t}"
    async with aiohttp.ClientSession() as client:
        async with client.get(url.format(endpoint=ENDPOINT, t=delay_seconds)) as res:
            return await res.json()


def fetch_data_delayed(delay_seconds: int):
    url = "http://{endpoint}/api/echodelay?t={t}"
    res = requests.get(url.format(endpoint=ENDPOINT, t=delay_seconds))
    return res.json()


def fetch_data_delayed_pprint(delay_seconds: int):
    url = "http://{endpoint}/api/echodelay?t={t}"
    res = requests.get(url.format(endpoint=ENDPOINT, t=delay_seconds))
    rj = res.json()
    print(f"{yel('delay')}: {rj['delay']}")


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


def _apply_color(s: str, ansi_color: str) -> str:
    return f"{ansi_color}{s}{Fore.RESET}"


def yel(s: str) -> str:
    return _apply_color(s, Fore.YELLOW)


def blu(s: str) -> str:
    return _apply_color(s, Fore.BLUE)
