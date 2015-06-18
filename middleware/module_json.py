from __future__ import unicode_literals

from urlparse import urljoin

import requests

def main(app, data):
    r = requests.get(data.get('api_url'))
    
    return r.json()
