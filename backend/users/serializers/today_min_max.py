import datetime

from pytz import utc

today_min = utc.localize(datetime.datetime.combine(datetime.date.today(), datetime.time.min))
today_max = utc.localize(datetime.datetime.combine(datetime.date.today(), datetime.time.max))
