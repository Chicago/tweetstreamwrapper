import calendar
import time

def map_tweet_fields(json_object):
	
	# If coordinates is not populated, then the tweet was either not geotagged or
	# it was captured in a bounding box. In either case, there will be no specific
	# POINT information (lat / lon) so we don't bother with processing
	if json_object['coordinates'] == None:
		return None
	
	response = {}
	response["id"] = str('ObjectId("' + json_object['id_str'] + '")')
	response["shard"] = json_object['coordinates']['coordinates'][0]
	response["what"] = {"text": json_object['text'], 
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
