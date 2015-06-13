import feedparser

def main(app, data):
    feed = feedparser.parse(data['rss_feed'])
    
    return feed

