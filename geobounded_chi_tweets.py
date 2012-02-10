from tweetstream import FilterStream
from tweetstream import ConnectionError, AuthenticationError, SampleStream
from couchdbkit import *

from twitter_user_info import user_info

#couchdb init
server = Server(uri='http://geopher.net:5984')
db = server.get_db('chicago_tweets')

# things to track
locations = ["-87.96,41.644", "-87.40,42.04"]
	
def start_stream():
    try:        
		with FilterStream(user_info['username'], user_info['password'], locations=locations) as stream:
			for tweet in stream:
				print "Got tweet %s from %-16s\t( tweet %d, rate %.1f tweets/sec)" % \
					(tweet["id_str"], tweet["user"]["screen_name"], stream.count, stream.rate ) 
				db[tweet["id_str"]] = dict(tweet)
    except KeyError, e:
		print "KeyError: ", e
		start_stream()
    except ResourceConflict, e:
		print "ResourceConflict: ", e
		start_stream()				
    except ConnectionError, e:
		print "Disconnected from twitter. Reason:", e.reason
        
start_stream()
