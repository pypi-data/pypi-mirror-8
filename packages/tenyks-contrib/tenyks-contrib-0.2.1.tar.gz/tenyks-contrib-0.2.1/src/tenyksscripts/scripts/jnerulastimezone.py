from datetime import datetime
from dateutil.tz import tzlocal
import pytz


def run(data, settings):
    if data['payload'] == 'current jnerula time':
        tz = pytz.timezone('Asia/Taipei')
        now = datetime.now(tzlocal())
        now.replace(tzinfo=tz)
        return now.astimezone(tz).strftime('%a %b %d %X %z')
