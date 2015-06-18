from __future__ import unicode_literals

from os import environ

import requests
import xmltodict

def main(app, data):
    url_data = {
        'method': 'flickr.people.getPhotos',
        'api_key': environ.get('FLICKR_KEY'),
        'user_id': data.get('nsid')
    }
    
    r = requests.post('https://api.flickr.com/services/rest/', data=url_data)
    
    return xmltodict.parse(r.content)
