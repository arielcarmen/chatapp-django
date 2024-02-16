from django.db import models
from db_connexion import db
import time
from bson import ObjectId

messages_collection = db['messages']


class DBMessageManager:
    def __init__(self):
        self.collection = messages_collection

    def create_message(self, contactId, discussionId, respondToMsgId, text, file):

        message_data = {
            "contactId": contactId,
            "discussionId": discussionId,
            "text": text,
            "responseToMsgId": respondToMsgId,
            "created_at" : time.time(),
            "reactions" : [],
            "file" : file,
        }
        return self.collection.insert_one(message_data)
    
    def find_by_id(self, id):
        return self.collection.find_one(ObjectId(id))