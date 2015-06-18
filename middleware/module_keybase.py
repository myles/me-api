from __future__ import unicode_literals

import requests


def main(app, data):
    r = requests.get('https://keybase.io/_/api/1.0/user/lookup.json',
                     data={'username': data.get('username')})

    return r.json()
