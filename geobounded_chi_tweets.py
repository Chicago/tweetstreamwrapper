from tweetils import * 
from database_manager import *
from twitter_user_info import user_info
from twitter_user_info import stop_words 

database_manager = DatabaseManager(user_info)        
app = Tweetils(database_manager, None, user_info, stop_words);
app.start_stream();

