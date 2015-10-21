import time
import datetime

try:
    from urlparse import urlparse, urlunparse
except ImportError:
    from urllib.parse import urlparse, urlunparse

import yaml

from flask.json import JSONEncoder
from flask.globals import current_app, request

from instagram import models as instagram_models


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):

        if isinstance(obj, time.struct_time):
            return datetime.datetime.fromtimestamp(time.mktime(obj))

        if isinstance(obj, datetime.date):
            return obj.isoformat()

        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        if isinstance(obj, datetime.time):
            return obj.isoformat()

        if isinstance(obj, instagram_models.ApiModel):
            return obj.__dict__

        return JSONEncoder.default(self, obj)


def remove_utm(url):
    parsed_url = list(urlparse(url))
    parsed_url[4] = '&'.join(
        [x for x in parsed_url[4].split('&') if not x.startswith('utm_')]
    )
    utmless_url = urlunparse(parsed_url)

    return utmless_url


def yamlify(*args, **kwargs):
    rv = current_app.response_class(
            yaml.safe_dump(
                dict(*args, **kwargs), line_break='\n',
                default_flow_style=False),
            mimetype="application/x-yaml")

    return rv
