from django.db import models
from db_connexion import db

messages_collection = db['messages']


class DBMessageManager:
    def __init__(self):
        self.collection = messages_collection

    def create_contact(self, user2Id):
        contact_data = {
            "user1Id": "65cd2c9425f598db480f1639",
            "user2Id": user2Id,
            "status": "PENDING",
            "user1Blocked": False,
            "user2Blocked": False,  
            "added_at" : time.time()
        }
        return self.collection.insert_one(messages_collection)