import pymongo
from pymongo import Connection
from tweetstream import FilterStream, ConnectionError, AuthenticationError, SampleStream
from tweetils import map_tweet_fields
from twitter_user_info import user_info

#open connection to mongo
connection = Connection(user_info['mongo_server'], user_info['mongo_port'])
db = connection.ops
db.authenticate(user_info['mongo_user'], user_info['mongo_password'])

# things to track
locations = ["-87.96,41.644", "-87.40,42.04"]

def start_stream():
    try:        
        with FilterStream(user_info['username'], user_info['password'], locations=locations) as stream:
            for tweet in stream:
	            print "Got tweet %s from %-16s\t( tweet %d, rate %.1f tweets/sec)" % \
									(tweet["id_str"], tweet["user"]["screen_name"], stream.count, stream.rate )
	            filtered_tweet = map_tweet_fields(dict(tweet))
	            if filtered_tweet != None:
		            db.twitter_test.insert(filtered_tweet)
    except KeyError, e:
		print "KeyError: ", e
		start_stream()
    except ConnectionError, e:
		print "Disconnected from twitter. Reason:", e.reason
        
start_stream()
