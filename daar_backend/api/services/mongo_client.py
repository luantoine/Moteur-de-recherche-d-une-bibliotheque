from pymongo import MongoClient
from django.conf import settings

class MongoDBClient:
    def __init__(self):
        connection_string = settings.MONGO_CONNEXION

        self.client = MongoClient(connection_string)
        self.db = self.client["Cluster0"]

    def get_collection(self, collection_name):
        return self.db[collection_name]

mongo_client = MongoDBClient()