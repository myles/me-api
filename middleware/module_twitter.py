from __future__ import unicode_literals

from os import environ

import tweepy


def main(app, data):
    auth = tweepy.OAuthHandler(environ.get('TWITTER_CONSUMER_KEY'),
                               environ.get('TWITTER_CONSUMER_SECRET'))
    auth.set_access_token(environ.get('TWITTER_ACCESS_TOKEN'),
                          environ.get('TWITTER_ACCESS_TOKEN_SECRET'))

    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    return api.me()
