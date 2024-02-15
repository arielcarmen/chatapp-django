from django.shortcuts import render
from .models import surveys_collection, DBSurveyManager
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from decorators import token_required
from utils import auth_user_id
import json, string, random
from bson import ObjectId

survey_manager = DBSurveyManager()
@csrf_exempt
@require_http_methods(["POST"])
@token_required
def add_survey(request):
    try:
        data = json.loads(request.body)
        discussionId = data['discussionId']
        question = data['question']
        options_data = data['options']
        options = []

        for op in options_data:
            data = {
                "id" : id_generator(),
                "response": op,
                "voters": []
            }
            options.append(data)

        result = survey_manager.create_survey(discussionId, question, options, auth_user_id(request))

        survey = survey_manager.find_by_id(result.inserted_id)
        survey['_id'] = str(survey['_id'])

        return JsonResponse({"data": survey}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["PATCH"])
@token_required
def response_survey(request, surveyId):
    try:
        data = json.loads(request.body)
        action = data['action']
        optionId = data['optionId']
        isSelected = data['isSelected']
        
        if action != "ASK_SURVEY":
            return JsonResponse({"error": "action invalide"}, status=400)
        else:
            filter = {"_id": ObjectId(surveyId), "options.id": optionId}
            if isSelected == True:
                update_query = {"$push": {"options.$.voters": {"$each": [auth_user_id(request)]}}}
                surveys_collection.update_one(filter, update_query)
                survey = survey_manager.find_by_id(surveyId)
                survey['_id'] = str(survey['_id'])
                return JsonResponse({"data": survey}, status=200)

            return JsonResponse({"data": "no new vote"}, status=200)
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
