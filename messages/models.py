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

        message_data = {
            "user1Id": "65cd2c9425f598db480f1639",
            "discussionId": "tbd",
            "text": user2Id,
            "responseToMsgId": "65cd2c9425f598db480f1639",
            "created_at" : time.time(),
            "reactions" : [],
            "file" : {
                "name": filename,
                "type": filetype,
                "pathUrl": filepath,
                "size": filesize
            }
        }
        return self.collection.insert_one(message_data)