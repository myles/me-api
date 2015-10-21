from __future__ import unicode_literals

import os

import yaml
import requests


def local(app, data):
    filepath = os.path.join(app.data_dir, data.get('filename'))

    with open(filepath, 'r') as f:
        contents = yaml.load(f)

    return contents


def remote(app, data):
    r = requests.get(data.get('url'))

    contents = yaml.load(r.data)

    return contents


def main(app, data):
    if data.get('filename'):
        return local(app, data)

    if data.get('url'):
        return remote(app, data)
