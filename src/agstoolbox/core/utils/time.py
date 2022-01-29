from datetime import datetime


def s_ago(ft: float) -> str:
    """
        Calculate a '3 hours ago' type string from a python datetime,
        if time less than 5 days, otherwise, return date as day/month/year
    """
    units = {
        'days': lambda diff: diff.days,
        'hours': lambda diff: diff.seconds / 3600,
        'minutes': lambda diff: diff.seconds % 3600 / 60,
    }
    t = datetime.utcfromtimestamp(ft)
    diff = datetime.utcnow() - t

    if diff.days >= 5:
        return t.strftime("%d/%m/%Y")

    for unit in units:
        dur = units[unit](diff)  # Run the lambda function to get a duration
        if dur > 0:
            unit = unit[:-dur] if dur == 1 else unit  # De-pluralize if duration is 1 ('1 day' vs
            # '2 days')
            return '%s %s ago' % (dur, unit)
    return 'just now'
