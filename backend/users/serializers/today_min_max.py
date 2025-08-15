import datetime

from pytz import utc

today_min = utc.localize(
    datetime.datetime.combine(datetime.datetime.now(tz=utc).date(), datetime.time.min),
)
today_max = utc.localize(
    datetime.datetime.combine(datetime.datetime.now(tz=utc).date(), datetime.time.max),
)
