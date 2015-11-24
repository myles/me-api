import feedparser


def main(app, data):
    feed = feedparser.parse(data.get('rss_feed'))

    return feed
