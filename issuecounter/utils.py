from __future__ import print_function

import datetime
import json
import sys


DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'


def print_error(s, exit_code=1):
    print('ERROR: {}'.format(s), file=sys.stderr, flush=True)
    sys.exit(exit_code)


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        else:
            return super(DateTimeEncoder, self).default(obj)


def extract_datetime(s):
    if isinstance(s, datetime.datetime):
        return s
    return datetime.datetime.strptime(s[:-3] + s[-2:], DATETIME_FORMAT)
