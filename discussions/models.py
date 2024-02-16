from django.db import models
from db_connexion import db
import time
from utils import auth_user_id
from bson import ObjectId

discussions_collection = db['discussions']

actions = ["ADD_USERS_GROUP","REMOVE_USERS_GROUP","UPDATE_GROUP_INFO","ARCHIVE","PIN","MUTE","LEAVE"]


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
                    "userId": ObjectId(creator_id),
                    "isAdmin": True,
                    "isPinned": False,
                    "hasNewNotif": False,
                    "isArchived": False,
                    "isMuted": False,
                    "added_at": time.time() 
                },
            ]

        }
        return self.collection.insert_one(discussion_data)
    
    def find_by_id(self, id):
        return self.collection.find_one(ObjectId(id))
    
    def new_member(self, id):
        return {
            "userId": ObjectId(id),
            "isAdmin": False,
            "isPinned": False,
            "hasNewNotif": False,
            "isArchived": False,
            "isMuted": False,
            "added_at": time.time() 
        }
