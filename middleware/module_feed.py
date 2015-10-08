import feedparser

from redcache import default_cache


def main(app, data):
    feed = feedparser.parse(data.get('rss_feed'))

    return feed
