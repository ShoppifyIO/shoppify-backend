from datetime import datetime


def datetime_to_string(date: datetime | None) -> str | None:
    if date is None:
        return None

    return date.strftime('%Y-%m-%dT%H:%M:%SZ')