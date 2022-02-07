import calendar
import time


def utc_time_str_to_unixtime(time_str: str, time_fmt: str) -> float:
    """Convert a UTC time string to UNIX time.

    Parameters
    ----------
    time_str: str
        The UTC time string
    time_fmt: str
        The format of time_str

    Returns
    -------
    time_unix: float
        The input time_str converted into UNIX time format
    """
    time_struct = time.strptime(time_str, time_fmt)
    time_unix = calendar.timegm(time_struct)
    return time_unix
