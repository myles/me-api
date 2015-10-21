from __future__ import unicode_literals

import os

import yaml


def main(app, data):
    filepath = os.path.join(app.data_dir, data.get('filename'))

    with open(filepath, 'r') as f:
        contents = yaml.load(f)

    return contents
