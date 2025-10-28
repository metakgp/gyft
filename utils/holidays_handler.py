from __future__ import annotations

import os
import json
from datetime import datetime
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup as bs

from utils.build_event import generate_india_time


CACHE_DIR = 'cache'


def ensure_cache_dir():
    if not os.path.isdir(CACHE_DIR):
        os.makedirs(CACHE_DIR, exist_ok=True)


def holidays_cache_path() -> str:
    ensure_cache_dir()
    year = datetime.today().year
    return os.path.join(CACHE_DIR, f"holidays_{year}.json")


def get_holidays(refresh: bool = False) -> List[Tuple[str, datetime]]:
    """
    Fetch IITKGP institute holidays with caching.

    Returns a list of tuples: (occasion, datetime_at_midnight_Asia_Kolkata)
    """
    cache_path = holidays_cache_path()

    if not refresh and os.path.isfile(cache_path):
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                raw = json.load(f)
                return [(r[0], generate_india_time(*r[1])) for r in raw]
        except Exception:
            pass

    url = "https://www.iitkgp.ac.in/holidays"
    result = requests.get(url, timeout=15).text
    doc = bs(result, "html.parser")
    tbody = doc.tbody
    trs = tbody.contents
    holidays: List[Tuple[str, datetime]] = []

    for i in range(3, len(trs) - 7, 2):
        cnt = 0
        occasion = None
        for tr in trs[i]:
            cnt += 1
            if cnt == 2:
                occasion = tr.string
            if cnt == 4:
                datetime_str = tr.string
                try:
                    dt = datetime.strptime(datetime_str, "%d.%m.%Y")
                    hol_date = generate_india_time(dt.year, dt.month, dt.day, 0, 0)
                    holidays.append((occasion, hol_date))
                except Exception:
                    continue

    holidays.sort(key=lambda x: x[1])

    # Cache as [[occasion, [year, month, day, hour, minute]], ...]
    try:
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump([[h[0], [h[1].year, h[1].month, h[1].day, 0, 0]] for h in holidays], f, indent=2)
    except Exception:
        pass

    return holidays
