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
            return JsonResponse({"error": "Invalid action"}, status=400)
        else:
            for id in members:
                update = {"$push": {"members": discussion_manager.new_member(id)}}
                discussions_collection.update_one(filter, update)
            
            discussion = discussion_manager.find_by_id(discussionId)
            discussion['_id'] = str(discussion['_id'])
            for member in discussion['members']:
                member['userId'] = str(member['userId'])

            return JsonResponse({"data": discussion}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["PATCH"])
@token_required
def update_group(request, discussionId):
    try:
        data = json.loads(request.body)
        action = data['action']
        name = data['name']
        description = data['description']

        if action not in actions:
            return JsonResponse({"error": "Invalid action"}, status=400)
        else:
            filter = {"_id": ObjectId(discussionId)}
            update = {"$set": {"description": description, "name": name}}
            discussions_collection.update_one(filter, update)
            discussion = discussion_manager.find_by_id(discussionId)
            discussion['_id'] = str(discussion['_id'])
            for member in discussion['members']:
                member['userId'] = str(member['userId'])
            
            return JsonResponse({"data": discussion}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["PATCH"])
@token_required
def pin_unpin_group(request, discussionId):
    try:
        data = json.loads(request.body)
        action = data['action']

        if action not in actions:
            JsonResponse({"error": "Invalid action"}, status=400)
        else:
            discussion = discussion_manager.find_by_id(discussionId)

            for member in discussion['members']:
                if member['userId'] == ObjectId(auth_user_id(request)):
                    isPinned = member.get('isPinned', False)

                    isPinned = not isPinned

                    discussions_collection.update_one(
                        {"_id": ObjectId(discussionId), "members.userId": ObjectId(auth_user_id(request))},
                        {"$set": {"members.$.isPinned": isPinned}}
                    )

                    discussion = discussion_manager.find_by_id(discussionId)
                    discussion['_id'] = str(discussion['_id'])
                    for member in discussion['members']:
                        member['userId'] = str(member['userId'])
                    
                    return JsonResponse({"data": discussion}, status=200)
                
            return JsonResponse({"error": "Not in discussion !"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["PATCH"])
@token_required
def archive_unarchive_discussion(request, discussionId):
    try:
        data = json.loads(request.body)
        action = data['action']

        if action not in actions:
            JsonResponse({"error": "Invalid action"}, status=400)
        else:
            discussion = discussion_manager.find_by_id(discussionId)

            for member in discussion['members']:
                if member['userId'] == ObjectId(auth_user_id(request)):
                    isArchived = member.get('isArchived')
                    isArchived = not isArchived

                    discussions_collection.update_one(
                        {"_id": ObjectId(discussionId), "members.userId": ObjectId(auth_user_id(request))},
                        {"$set": {"members.$.isArchived": isArchived}}
                    )

                    discussion = discussion_manager.find_by_id(discussionId)
                    discussion['_id'] = str(discussion['_id'])
                    for member in discussion['members']:
                        member['userId'] = str(member['userId'])
                    
                    return JsonResponse({"data": discussion}, status=200)
                
            return JsonResponse({"error": "Not in discussion !"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["PATCH"])
@token_required
def mute_unmute_discussion(request, discussionId):
    try:
        data = json.loads(request.body)
        action = data['action']

        if action not in actions:
            JsonResponse({"error": "Invalid action"}, status=400)
        else:
            discussion = discussion_manager.find_by_id(discussionId)

            for member in discussion['members']:
                if member['userId'] == ObjectId(auth_user_id(request)):
                    isMuted = member.get('isMuted')
                    isMuted = not isMuted

                    discussions_collection.update_one(
                        {"_id": ObjectId(discussionId), "members.userId": ObjectId(auth_user_id(request))},
                        {"$set": {"members.$.isMuted": isMuted}}
                    )

                    discussion = discussion_manager.find_by_id(discussionId)
                    discussion['_id'] = str(discussion['_id'])
                    for member in discussion['members']:
                        member['userId'] = str(member['userId'])
                    
                    return JsonResponse({"data": discussion}, status=200)
                
            return JsonResponse({"error": "Not in discussion !"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["PATCH"])
@token_required
def remove_user_group(request, discussionId):
    try:
        data = json.loads(request.body)
        filter = {"_id": ObjectId(discussionId)}

        members = data['members']
        action = data['action']

        if action not in actions:
            return JsonResponse({"error": "Invalid action"}, status=400)
        else:
            for id in members:
                update = {"$pull": {"members": {"userId": ObjectId(id)}}}
                discussions_collection.update_one(filter, update)
            
            discussion = discussion_manager.find_by_id(discussionId)
            discussion['_id'] = str(discussion['_id'])
            for member in discussion['members']:
                member['userId'] = str(member['userId'])

            return JsonResponse({"data": discussion}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["PATCH"])
@token_required
def leave_discussion(request, discussionId):
    try:
        data = json.loads(request.body)
        filter = {"_id": ObjectId(discussionId)}

        action = data['action']

        if action not in actions:
            return JsonResponse({"error": "Invalid action"}, status=400)
        else:
            update = {"$pull": {"members": {"userId": ObjectId(auth_user_id(request))}}}
            discussions_collection.update_one(filter, update)
            
            discussion = discussion_manager.find_by_id(discussionId)
            discussion['_id'] = str(discussion['_id'])
            for member in discussion['members']:
                member['userId'] = str(member['userId'])

            return JsonResponse({"data": discussion}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["GET"])
@token_required
def get_discussion(request, discussionId):
    try:
        discussion_manager.find_by_id(discussionId)

        discussion = discussion_manager.find_by_id(discussionId)
        discussion['_id'] = str(discussion['_id'])
        for member in discussion['members']:
            member['userId'] = str(member['userId'])

        return JsonResponse({"data": discussion}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["DELETE"])
@token_required
def delete_group(request,discussionId):
    try:
        discussion_manager.find_by_id(discussionId)

        discussion = discussion_manager.find_by_id(discussionId)
        discussion['_id'] = str(discussion['_id'])
        for member in discussion['members']:
            member['userId'] = str(member['userId'])

        filter = {"_id": ObjectId(discussionId)}
        discussions_collection.delete_one(filter)

        return JsonResponse({"data": discussion}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["PATCH"])
@token_required
def open_discussion(request,discussionId):
    try:
        discussion_manager.find_by_id(discussionId)

        for member in discussion['members']:
            if member['userId'] == ObjectId(auth_user_id(request)):
                discussions_collection.update_one(
                    {"_id": ObjectId(discussionId), "members.userId": ObjectId(auth_user_id(request))},
                    {"$set": {"members.$.hasNewNotif": True}}
                )
        discussion = discussion_manager.find_by_id(discussionId)
        discussion['_id'] = str(discussion['_id'])
        for member in discussion['members']:
            member['userId'] = str(member['userId'])

        filter = {"_id": ObjectId(discussionId)}
        discussions_collection.delete_one(filter)

        return JsonResponse({"data": discussion}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)