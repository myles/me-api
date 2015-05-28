import feedparser

def main(data):
    feed = feedparser.parse(data['rss_feed'])
    
    return feed

