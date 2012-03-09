from tweetils import * 
from database_manager import *
from twitter_user_info import user_info

database_manager = DatabaseManager(user_info)        
app = Tweetils(database_manager, None, user_info);
app.start_stream();

