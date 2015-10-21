from __future__ import unicode_literals

import os

import json
import requests


def local(app, data):
    filepath = os.path.join(app.data_dir, data.get('filename'))

    with open(filepath, 'r') as f:
        contents = json.loads(f)

    return contents


def remote(app, data):
    r = requests.get(data.get('api_url'))

    return r.json()


def main(app, data):
    if data.get('filename'):
        return local(app, data)

    if data.get('url'):
        return remote(app, data)
