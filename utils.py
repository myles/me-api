import time
import datetime

from tweepy.api import API as tweepy_api

from flask.json import JSONEncoder

class CustomJSONEncoder(JSONEncoder):
    
    def default(self, obj):
        
        if isinstance(obj, time.struct_time):
            return datetime.datetime.fromtimestamp(time.mktime(obj))
        
        if isinstance(obj, tweepy_api):
            return None
        
        return JSONEncoder.default(self, obj)
