import unittest
import json
from tweetils import map_tweet_fields

class TestSequenceFunctions(unittest.TestCase):
	                
    def setUp(self):
        # load a sample tweet into memory to test with
        tweet = open('testdata/test_tweet.json', 'r').read()
        self.test_tweet = json.loads(tweet)

    def test_that_map_tweet_fields_proccesses_tweet(self):
        response = map_tweet_fields(self.test_tweet)
        self.assertEqual('ObjectId("170009469021982720")', response["id"])
        self.assertEqual(-89.82472222, response["shard"])
        what = response['what']
        self.assertEqual('talk about the weather', what["text"])
        self.assertEqual(23, what["retweet_count"])
        self.assertEqual(21, what["followers_count"])
        self.assertEqual("unsuccess", what["hashtags"][0]["text"])
        where = response['where']
        self.assertEqual(40.0075, where["location"][0])
        self.assertEqual(-89.82472222, where["location"][1])
        self.assertEqual(1329368390, response["when"]["date"])
        who = response['who']
        self.assertEqual(165964121, who["id"])
        self.assertEqual("WoodlandLakesWS", who["screen_name"])
        self.assertEqual("Weather Conditions...", who["description"])
        self.assertEqual("Petersburg, IL USA", who["location"])
        self.assertEqual("TWEET", response["type"])

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
	unittest.TextTestRunner(verbosity=2).run(suite)
	