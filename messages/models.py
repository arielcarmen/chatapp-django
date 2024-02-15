from django.db import models
from db_connexion import db
import time

messages_collection = db['messages']


class DBMessageManager:
    def __init__(self):
        self.collection = messages_collection

    def create_message(self, user2Id):
        filename = ""
        filetype = ""
        filepath = ""
        filesize = ""

        contact_data = {
            "user1Id": "65cd2c9425f598db480f1639",
            "text": user2Id,
            "responseToMsgId": "PENDING",
            "created_at" : time.time(),
            "file" : {
                "name": filename,
                "type": filetype,
                "pathUrl": filepath,
                "size": filesize
            }
        }
        return self.collection.insert_one(messages_collection)