from __future__ import unicode_literals

from os import environ

import requests
import xmltodict


def main(app, data):
    url_data = {
        'method': 'flickr.people.getPhotos',
        'api_key': environ.get('FLICKR_KEY'),
        'user_id': data.get('nsid'),
        'extras': 'description, license, date_upload, date_taken, ' +
                  'owner_name, icon_server, original_format, last_update, ' +
                  'geo, tags, machine_tags, o_dims, views, media, ' +
                  'path_alias, url_sq, url_t, url_s, url_q, url_m, url_n, ' +
                  'url_z, url_c, url_l, url_o'
    }

    r = requests.post('https://api.flickr.com/services/rest/', data=url_data)

    return xmltodict.parse(r.content)
