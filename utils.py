import time
import datetime

from flask.json import JSONEncoder

from instagram import models as instagram_models


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):

        if isinstance(obj, time.struct_time):
            return datetime.datetime.fromtimestamp(time.mktime(obj))

        if isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")

        if isinstance(obj, instagram_models.ApiModel):
            return obj.__dict__

        return JSONEncoder.default(self, obj)
