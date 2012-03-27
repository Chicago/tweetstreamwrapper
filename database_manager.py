import pymongo
from collections import deque
from pymongo import Connection
from pymongo.errors import *

class DatabaseManager(object):

    def __init__(self, configuration_list):
        self.configs = configuration_list
        self.connection = None
        self.db = None
        self.active = False
        self.message_queue = deque()
        self.connect()

    def connect(self):
        try: 
            self.connection = Connection(self.configs['mongo_server'], self.configs['mongo_port'])
            self.db = self.connection.ops
            self.db.authenticate(self.configs['mongo_user'], self.configs['mongo_password']) 
            print "connected to mongodb!"
            self._empty_queue()
            self.active = True
        except Exception, e:
           print "Database Manager Exception: ", e
           self.active = False

    def insert(self, document):
        # guard clause: if we have no connection to db then
        # queue document and try to connect to db again
        if not self.active:
            self._add_to_queue(document)   
            self.connect()
            return
        try:
            self.db.twitter_test.insert(document, safe=True)
        except (IOError, OperationFailure), e:
            print "DatabaseManger Socket Error: ", e
            self.active = False

    def _empty_queue(self):
        if len(self.message_queue) == 0:
            return
        for document in self.message_queue:
            print "inserting queued document with id {0}".format(document["_id"])
            self.db.twitter_test.insert(document, safe=True)
        self.message_queue.clear()
        print "DatabaseManager queue has been cleared - all messages written to mongodb"

    def _add_to_queue(self, document):
        if len(self.message_queue) >= 25000:
            raise BufferError("DatabaseManager cannot queue anymore")

        self.message_queue.append(document) 
        print "database is unavailable {0} tweets now in queue".format(len(self.message_queue))

