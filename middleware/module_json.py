from __future__ import unicode_literals

import requests


def main(app, data):
    r = requests.get(data.get('api_url'))

    return r.json()
