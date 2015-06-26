from __future__ import unicode_literals

from os import environ

from instagram.client import InstagramAPI


def main(app, data):
    api = InstagramAPI(client_id=environ.get('INSTAGRAM_CLIENT_ID'), client_secret=environ.get(
        'INSTAGRAM_CLIENT_SECRET'), access_token=environ.get('INSTAGRAM_ACCESS_TOKEN'))

    user = api.user().__dict__

    recent_media, next_ = api.user_recent_media()

    user['media'] = []

    for media in recent_media:
        user['media'] += [media, ]

    return user
