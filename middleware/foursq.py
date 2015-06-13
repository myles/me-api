from __future__ import unicode_literals

from os import environ

from foursquare import Foursquare

def main(app, data):
    api = Foursquare(client_id=environ.get('FOURSQUARE_CLIENT_ID'), client_secret=environ.get('FOURSQUARE_CLIENT_SECRET'), access_token=environ.get('FOURSQUARE_ACCESS_TOKEN'))
    
    return api.users.checkins()