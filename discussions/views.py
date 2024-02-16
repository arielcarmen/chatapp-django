from django.shortcuts import render
from .models import discussions_collection
from django.http import HttpResponse
from .models import discussions_collection, DBDiscussionManager, actions
import json
from django.http import JsonResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from decorators import token_required
from utils import auth_user_id
from bson import ObjectId

discussion_manager = DBDiscussionManager()

@csrf_exempt
@require_http_methods(["POST"])
@token_required
def create_discussion(request):
    try:
        data = json.loads(request.body)
        result = discussion_manager.create_discussion(auth_user_id(request))
        discussion = discussion_manager.find_by_id(result.inserted_id)
        discussion['_id'] = str(discussion['_id'])

        return JsonResponse({"data": discussion}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["GET"])
@token_required
def discussions(request):
    try:
        data = json.loads(request.body)
        filter = {"members.userId": ObjectId(auth_user_id(request))}
        discussions = list(discussions_collection.find(filter))
        for discussion in discussions:
            discussion['_id'] = str(discussion['_id'])

        return JsonResponse({"data": discussions}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["GET"])
@token_required
def archived_discussions(request):
    try:
        data = json.loads(request.body)
        filter = {"members.userId": ObjectId(auth_user_id(request)), "members.isArchived" : True}
        discussions = list(discussions_collection.find(filter))
        for discussion in discussions:
            discussion['_id'] = str(discussion['_id'])

        return JsonResponse({"data": discussions}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["GET"])
@token_required
def pinned_discussions(request):
    try:
        data = json.loads(request.body)
        filter = {"members.userId": ObjectId(auth_user_id(request)), "members.isPinned" : True}
        discussions = list(discussions_collection.find(filter))
        for discussion in discussions:
            discussion['_id'] = str(discussion['_id'])

        return JsonResponse({"data": discussions}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["PATCH"])
@token_required
def add_user_group(request, discussionId):
    try:
        data = json.loads(request.body)
        filter = {"_id": ObjectId(discussionId)}

        members = data['members']
        action = data['action']

        if action not in actions:
            return JsonResponse({"message": "Invalid action"}, status=400)
        else:
            for id in members:
                update = {"$push": {"members": discussion_manager.new_member(id)}}
                discussions_collection.update_one(filter, update)
            
            discussion = discussion_manager.find_by_id(discussionId)
            discussion['_id'] = str(discussion['_id'])

            return JsonResponse({"data": discussion}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["PATCH"])
@token_required
def update_group(request):
    try:
        data = json.loads(request.body)
        email = data['email']

        return JsonResponse({"message": "status mis a jour"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["PATCH"])
@token_required
def pin_unpin_group(request):
    try:
        data = json.loads(request.body)
        email = data['email']

        return JsonResponse({"message": "status mis a jour"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["PATCH"])
@token_required
def archive_unarchive_discussion(request):
    try:
        data = json.loads(request.body)
        email = data['email']

        return JsonResponse({"message": "status mis a jour"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["PATCH"])
@token_required
def mute_unmute_discussion(request):
    try:
        data = json.loads(request.body)
        email = data['email']

        return JsonResponse({"message": "status mis a jour"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["PATCH"])
@token_required
def remove_user_group(request):
    try:
        data = json.loads(request.body)
        email = data['email']

        return JsonResponse({"message": "status mis a jour"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["PATCH"])
@token_required
def leave_discussion(request):
    try:
        data = json.loads(request.body)
        email = data['email']

        return JsonResponse({"message": "status mis a jour"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["PATCH"])
@token_required
def open_discussion(request):
    try:
        data = json.loads(request.body)
        email = data['email']

        return JsonResponse({"message": "status mis a jour"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["DELETE"])
@token_required
def delete_group(request):
    try:
        data = json.loads(request.body)
        email = data['email']

        return JsonResponse({"message": "status mis a jour"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)