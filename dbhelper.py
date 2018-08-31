import os
import pymongo

uri = os.environ['uri']

DATABASE = 'engsci2t2timetables'


class DBHelper:
    def __init__(self):
        client = pymongo.MongoClient(uri)
        self.db = client[DATABASE]

    def get_user(self, name):
        return self.db.users.find_one({'name': name})

    def add_user(self, name, timetable):
        self.db.users.insert({'name': name, 'timetable': timetable})
