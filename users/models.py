from django.db import models
from werkzeug.security import generate_password_hash, check_password_hash
from db_connexion import db
from bson import ObjectId

users_collection = db['users']

class DBUserManager:
    def __init__(self):
        self.collection = db['users']

    def create_user(self, firstname, lastname, email, password):
        hashed_password = generate_password_hash(password)
        user_data = {
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "password": hashed_password,
            "photoUrl": None,
            "status": None
        }
        return self.collection.insert_one(user_data)

    def find_user_by_email(self, email):
        return self.collection.find_one({"email": email})
    
    def find_by_id(self, id):
        return self.collection.find_one({"_id": ObjectId(id)})
    
    def check_password(self, email, password):
        user = self.find_user_by_email(email)
        if user:
            return check_password_hash(user['password'], password)
        return False
