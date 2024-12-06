from datetime import datetime

import pytz


def remove_non_args(**kwargs):
    return {field: value for field, value in kwargs.items() if value is not None}


def convert_to_israel_time(utc_time: datetime) -> datetime:
    israel_time_zone = pytz.timezone("ASIA/Jerusalem")
    return utc_time.astimezone(israel_time_zone)