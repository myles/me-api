import time
import datetime

from flask.json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):

        if isinstance(obj, time.struct_time):
            return datetime.datetime.fromtimestamp(time.mktime(obj))

        if isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")

        return JSONEncoder.default(self, obj)
