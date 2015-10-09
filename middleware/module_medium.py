from __future__ import unicode_literals

import requests

try:
    import json
except ImportError:
    import simplejson as json


def main(app, data):
    r = requests.get('https://medium.com/%s?format=json' %
                     data.get('username'))

    response_content = r.content.decode('utf-8')

    json_data = response_content.lstrip('])}while(1);</x>')

    return json.loads(json_data)
