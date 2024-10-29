import datetime

from django.utils.timezone import get_default_timezone
from pytz import utc

today_min = utc.localize(
    datetime.datetime.combine(
        datetime.datetime.now(tz=get_default_timezone()).date(),
        datetime.time.min,
    ),
)
today_max = utc.localize(
    datetime.datetime.combine(
        datetime.datetime.now(tz=get_default_timezone()).date(),
        datetime.time.max,
    ),
)
