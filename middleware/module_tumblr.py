from __future__ import unicode_literals

from urlparse import urljoin

import requests

def main(app, data):
    r = requests.get(urljoin(data.get('tumblr_url'), '/api/read/json?debug=1'))
    
    return r.json()
