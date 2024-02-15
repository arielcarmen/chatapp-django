from django.db import models
from db_connexion import db
import time
from utils import auth_user_id
from bson import ObjectId

discussions_collection = db['discussions']


class DBDiscussionManager:
    def __init__(self):
        self.collection = discussions_collection

    def create_discussion(self, creator_id):
        discussion_data = {
            "tag": "GROUP",
            "name": "Groupe 1",
            "description": "description group",
            "members" : [
                {
                    "userId": creator_id,
                    "isAdmin": True
                },
            ]

        }
        return self.collection.insert_one(discussion_data)
    
    def find_by_id(self, id):
        return self.collection.find_one(ObjectId(id))
