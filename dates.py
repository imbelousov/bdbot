#!/usr/bin/env python
import datetime
import time


def today() -> datetime.date:
    return timestamp_to_date(time.time())


def parse_date(string: str) -> datetime.date:
    return datetime.datetime.strptime(string, "%d.%m.%Y")


def timestamp_to_date(ts: int) -> datetime.date:
    return datetime.date.fromtimestamp(ts)


def date_to_timestamp(dt: datetime.date) -> int:
    return time.mktime(dt.timetuple())


def calc_next_birthday(dt: datetime.date) -> datetime.date:
    while dt < today():
        dt = datetime.date(dt.year + 1, dt.month, dt.day)
    return dt
