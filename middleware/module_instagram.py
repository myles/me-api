from __future__ import unicode_literals

from os import environ

from instagram.client import InstagramAPI

def main(app, data):
    api = InstagramAPI(client_id=environ.get('INSTAGRAM_CLIENT_ID'), client_secret=environ.get('INSTAGRAM_CLIENT_SECRET'), access_token=environ.get('INSTAGRAM_ACCESS_TOKEN'))
    
    user = api.user().__dict__
    
    recent_media, next_ = api.user_recent_media()
    
    user['media'] = []
    
    for media in recent_media:
        data = {}
        data['id'] = media.id
        data['type'] = media.type
        data['caption'] = str(media.caption)
        data['link'] = media.link
        data['standard_resolution'] = media.get_standard_resolution_url()
        data['low_resolution'] = media.get_low_resolution_url()
        data['thumbnail'] = media.get_thumbnail_url()
        
        user['media'] += [data,]
    
    return user