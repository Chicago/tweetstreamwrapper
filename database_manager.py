import pymongo
from pymongo import Connection

class DatabaseManager(object):

    def __init__(self, configuration_list):
        connection = Connection(configuration_list['mongo_server'], configuration_list['mongo_port'])
        self.db = connection.ops
        self.db.authenticate(configuration_list['mongo_user'], configuration_list['mongo_password'])

    def insert(self, document):
        self.db.twitter_test.insert(document)
