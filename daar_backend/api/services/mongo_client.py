from pymongo import MongoClient
from django.conf import settings

class MongoDBClient:
    def __init__(self):
        try:
            connection_string = settings.MONGO_CONNEXION
            self.client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
            self.db = self.client["Cluster0"]
            # Test de la connexion
            self.client.admin.command("ping")
        except Exception as e:
            raise Exception(f"Erreur de connexion à MongoDB : {e}")

    def get_collection(self, collection_name):
        return self.db[collection_name]

mongo_client = MongoDBClient()