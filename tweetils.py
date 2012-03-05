import calendar
import time
import pymongo
from pymongo import Connection
from tweetstream import FilterStream, ConnectionError, AuthenticationError, SampleStream

class Tweetils(object):

    def __init__(self, database_manager, configuration_list):
        self.db = database_manager
        self.user_info = configuration_list

    def start_stream(self):
        try:
            with FilterStream(self.user_info["username"],
                              self.user_info["password"], 
                              locations=self.user_info["locations"]) as stream:
                for tweet in stream:
                    print "Got tweet %s from %-16s\t( tweet %d, rate %.1f tweets/sec)" % \
                        (tweet["id_str"], tweet["user"]["screen_name"], stream.count, stream.rate)
                    filtered_tweet = self.map_tweet_fields(dict(tweet))
                    if filtered_tweet != None:
                            self.db.insert(filtered_tweet)
        except KeyError, e:
            print "KeyError: ", e
            self.start_stream()
        except ConnectionError, e:
            print "Disconnected from twitter. Reason:", e.reason
            print "timing out for 10 seconds..."
            time.sleep(10)
            print "restarting"
            self.start_stream()

    def map_tweet_fields(self, json_object):

        # If coordinates is not populated, then the tweet was either not geotagged or
	# it was captured in a bounding box. In either case, there will be no specific
	# POINT information (lat / lon) so we don't bother with processing
	if json_object['coordinates'] == None:
		return None
	
        # build response dict based on custom mongo/sharding scheme for City of Chi	
        response = {}
	response["id"] = str('ObjectId("' + json_object['id_str'] + '")')
	response["shard"] = json_object['coordinates']['coordinates'][0]
	response["what"] = {"text": json_object['text'],
                            "tag": self.user_info["tag"],
	                    "retweet_count": json_object['retweet_count'],
	                    "followers_count": json_object['user']['followers_count'],
	                    "hashtags": json_object['entities']['hashtags']}
	lat = json_object['coordinates']['coordinates'][1]
	lon = json_object['coordinates']['coordinates'][0]
	response["where"] = {"location": [lat, lon]}
	timestamp = time.strptime(json_object['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
	response["when"] = {"date": calendar.timegm(timestamp)}
	response["who"] = {"id": json_object['user']['id'], 
	                   "screen_name": json_object['user']['screen_name'],
	                   "description": json_object['user']['description'],
	                   "location": json_object['user']['location']}
	response["type"] = "TWEET"
	
	return response

class DatabaseManager(object):

    def __init__(self, configuration_list):
        connection = Connection(configuration_list['mongo_server'], configuration_list['mongo_port'])
        self.db = connection.ops
        self.db.authenticate(configuration_list['mongo_user'], configuration_list['mongo_password'])

    def insert(self, document):
        self.db.twitter_test.insert(document)

