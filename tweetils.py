import calendar
import json
import re
import time
from pymongo import *
from bson.binary import Binary
from time import gmtime, strftime
from whoosh.analysis import RegexTokenizer
from whoosh.analysis import LowercaseFilter
from whoosh.analysis import StopFilter
from tweetstream import FilterStream, ConnectionError, AuthenticationError, SampleStream

class Tweetils(object):

    def __init__(self, database_manager, publisher, configuration_list, stop_words):
        self.db = database_manager
        self.user_info = configuration_list
        self.publisher = publisher
        self.filter = RegexTokenizer() | \
           LowercaseFilter() | \
           StopFilter() | \
           StopFilter(stop_words)

    def start_stream(self):
        try:
            with FilterStream(self.user_info["username"],
                              self.user_info["password"], 
                              locations=self.user_info["locations"]) as stream:
                for tweet in stream:
                    print "%s Got tweet %s from %-16s\t( tweet %d, rate %.1f tweets/sec)" % \
                        (strftime("%Y%m%d %H:%M:%S +0000: ", gmtime()), tweet["id_str"], tweet["user"]["screen_name"], \
                        stream.count, stream.rate)
                    filtered_tweet = self.map_tweet_fields(dict(tweet))
                    if filtered_tweet != None:
                            print "attempting db insert and publish for {0}".format(tweet["id_str"])
                            if self.db != None:
                                self.db.insert(filtered_tweet)
                            if self.publisher != None:
                                self.publisher.publish(json.dumps(filtered_tweet))
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
	response['_id'] = json_object['id_str'] 
	response['shard'] = json_object['coordinates']['coordinates'][0]
        (stripped_text, link_array) = self.strip_links(json_object['text'])
        tokens = [token.text for token in self.filter(stripped_text)]
	response['what'] = {'text': json_object['text'],
                            'tokens': tokens,
                            'link_array': link_array,
                            'tag': self.user_info['tag'],
	                    'retweet_count': json_object['retweet_count'],
	                    'followers_count': json_object['user']['followers_count'],
	                    'hashtags': json_object['entities']['hashtags']}
	lat = json_object['coordinates']['coordinates'][1]
	lon = json_object['coordinates']['coordinates'][0]
	response['where'] = {'location': [lat, lon],
                             "latitude" : lat, 
                             "longitude" : lon}
	timestamp = time.strptime(json_object['created_at'], 
                                      '%a %b %d %H:%M:%S +0000 %Y')
	response['when'] = {'date': calendar.timegm(timestamp) * 1000, 
                        'shardtime': calendar.timegm(timestamp) * 1000}
	response['who'] = {'id': json_object['user']['id'], 
	                   'screen_name': json_object['user']['screen_name'],
	                   'description': json_object['user']['description'],
	                   'location': json_object['user']['location']}
	response['type'] = 'tweet'
	
        return response

    def strip_links(self, status):
        links = re.findall(r'(https?://\S+)', status)
        for url in links:
            status = status.replace(url, '')
        return (status, links)

