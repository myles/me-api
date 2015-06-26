from __future__ import unicode_literals

from urlparse import urljoin

import requests


def main(app, data):
    user = requests.get(urljoin('https://api.github.com/users/',
                        data.get('username'))).json()

    repos = requests.get(urljoin('https://api.github.com/users/',
                         data.get('username'), 'repos')).json()

    user['repos'] = repos

    return user
