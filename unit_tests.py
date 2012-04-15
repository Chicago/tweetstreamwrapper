import unittest
import json
from database_manager import *
from tweetils import Tweetils
from twitter_user_info import user_info

class MockDatabaseManager(object):

    def __init__(self):
        pass

    def insert(self, document):
        #mock object no op
        pass

class TestSequenceFunctions(unittest.TestCase):
	                
    def setUp(self):
        # load a sample tweet into memory to test with
        tweet = open('testdata/test_tweet.json', 'r').read()
        self.test_tweet = json.loads(tweet)
        mock_db_manager = MockDatabaseManager()
        mock_configuration = { "tag": "Chicago" }
        mock_stop_words = ['is', 'a']
        self.tweetils = Tweetils(mock_db_manager, None, mock_configuration,
            mock_stop_words)

    def test_that_map_tweet_fields_proccesses_tweet(self):
        response = self.tweetils.map_tweet_fields(self.test_tweet)
        self.assertEqual('170009469021982720', response["_id"])
        self.assertEqual(-89.82472222, response["shard"])
        what = response['what']
        self.assertEqual('talk about the weather http://www.weather.com/test', what["text"])
        self.assertEqual(['http://www.weather.com/test'], what["link_array"])
        self.assertEqual(23, what["retweet_count"])
        self.assertEqual(21, what["followers_count"])
        self.assertEqual("unsuccess", what["hashtags"][0]["text"])
        self.assertEqual([ "talk", "about", "weather" ], what['tokens'])
        self.assertEqual("Chicago", what["tag"])
        where = response['where']
        self.assertEqual(40.0075, where["location"][0])
        self.assertEqual(-89.82472222, where["location"][1])
        self.assertEqual('NumberLong("1329368390")', response["when"]["shardtime"])
        self.assertEqual('NumberLong("1329368390")', response["when"]["date"])
        who = response['who']
        self.assertEqual(165964121, who["id"])
        self.assertEqual("WoodlandLakesWS", who["screen_name"])
        self.assertEqual("Weather Conditions...", who["description"])
        self.assertEqual("Petersburg, IL USA", who["location"])
        self.assertEqual("tweet", response["type"])

    def test_that_strip_links_removes_uris(self):
        test_string = "check out my tweet http://t.co/NOZtxyAa #WAT!" \
            "https://chitown.gov/totally_fake.php/page$99~"
        expected_string = "check out my tweet  #WAT!"
        expected_array = ["http://t.co/NOZtxyAa", 
            "https://chitown.gov/totally_fake.php/page$99~"]
        (stripped_string, link_array) = self.tweetils.strip_links(test_string)
        self.assertEqual(stripped_string, expected_string)
        self.assertEqual(link_array, expected_array)

    def test_that_DBManage_handles_mongo_unique_index_error(self):
        database_manager = DatabaseManager(user_info)
        tweet = self.tweetils.map_tweet_fields(self.test_tweet)
        database_manager.insert(tweet)
        database_manager.insert(tweet)
  

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
	unittest.TextTestRunner(verbosity=2).run(suite)
