from __future__ import annotations  # for python 3.8
from datetime import datetime, timedelta


def internal_s_ago(t: datetime, diff: timedelta):
    """
        Calculate a '3 hours ago' type string from a python datetime,
        if time less than 5 days, otherwise, return date as day/month/year
    """
    units = {
        'days': lambda diff_t: diff_t.days,
        'hours': lambda diff_t: int(diff_t.seconds / 3600),
        'minutes': lambda diff_t: int(diff_t.seconds % 3600 / 60),
    }

    if diff.days >= 5:
        return t.strftime("%d/%m/%Y")

    for unit in units:
        dur = units[unit](diff)  # Run the lambda function to get a duration
        if dur > 0:
            # if duration is 1 ('1 day' vs '2 days')
            unit = unit[:-dur] if dur == 1 else unit  # De-pluralize
            return '%s %s ago' % (dur, unit)
    return 'just now'


def s_ago(ft: float) -> str:
    t = datetime.utcfromtimestamp(ft)
    diff = datetime.utcnow() - t

    return internal_s_ago(t, diff)
