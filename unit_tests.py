import unittest
from tweetils import get_intersection

class TestSequenceFunctions(unittest.TestCase):
	                
    def setUp(self):
        # mock tweet dict with id, id_str, and user fields
        # user field has two nested subfields; id and profile_text_color
        self.tweet = {'id': 167978744684883968, 
                      'id_str': "167978744684883968", 
                      'user': {'id': "196784134", "profile_text_color": "333333"}}

        # white_list (filter list) specifies that we want ALL information for id
        # that is, even if id has nested fields we will take them all
        # the filter also says that we want data from the user field but ONLY
        # the id nested field (so, the above mock object's profile_test_color should be
        # ignored)
        self.white_list = {'id': None, 'user': {'id': ''}}

    def test_union_filter_should_return_only_id_and_user_id(self):
        self.assertEqual('id' in self.tweet, True)
        expected = {'id': 167978744684883968, 
                    'user': {'id': '196784134'}}
        self.assertEqual(expected, get_intersection(self.tweet, self.white_list))

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
	unittest.TextTestRunner(verbosity=2).run(suite)
	