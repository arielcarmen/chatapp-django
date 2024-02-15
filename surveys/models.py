from django.db import models
import time
from bson import ObjectId

from db_connexion import db

surveys_collection = db['surveys']

class DBSurveyManager:
    def __init__(self):
        self.collection = surveys_collection

    def create_survey(self, discussionId, question, options, created_by):
        survey_data = {
            "discussionId": discussionId,
            "question": question,
            "options": options,
            "created_by" : created_by,
            "createdAt": time.time()
        }
        return self.collection.insert_one(survey_data)
    
    def find_by_id(self, id):
        return self.collection.find_one(ObjectId(id))
