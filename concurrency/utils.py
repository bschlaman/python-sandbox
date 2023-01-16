import concurrent.futures
import requests
import time

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

