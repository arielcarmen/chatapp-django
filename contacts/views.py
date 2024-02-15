from django.shortcuts import render
from .models import contacts_collection
from django.http import HttpResponse
import json
from .models import contacts_collection, DBContactManager
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from decorators import token_required
from bson import ObjectId, json_util
import jwt
from utils import auth_user_id

contact_manager = DBContactManager()


@csrf_exempt
@require_http_methods(["POST"])
@token_required
def send_request(request):
    try:
        data = json.loads(request.body)
        user2Id = data['user2Id']
        result = contact_manager.create_contact(user2Id= user2Id)

        contact_id = result.inserted_id
        contact = contacts_collection.find_one(contact_id)
        contact['_id'] = str(contact['_id'])
        
        return JsonResponse({"data":contact}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["PATCH"])
@token_required
def response_request(request, contactId):
    try:
        data = json.loads(request.body)
        status = data['status']
        action = data['action']

        if action not in ["ANSWER_TO_REQUEST", "BLOCK_CONTACT"]:
            return JsonResponse({"error": "Invalid action"}, status=400)
        
        if status not in ["VALIDATED", "DECLINED"]:
            return JsonResponse({"error": "Invalid status"}, status=400)
        
        filter = {'_id': ObjectId(contactId)}
        data = {'$set': {'status': status}}

        contacts_collection.update_one(filter, data)

        contact = contacts_collection.find_one(ObjectId(contactId))

        contact['_id'] = str(contact['_id'])

        return JsonResponse({"data":contact}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["GET"])
@token_required
def validated_contacts(request):
    try:

        status = request.GET.get('status', None)

        if status not in ["VALIDATED", "DECLINED", "PENDING"]:
            return JsonResponse({"error": "Invalid status"}, status=400)

        contacts = contacts_collection.find({
            'status': status,
        })

        documents = [doc for doc in list(contacts)]

        for doc in documents:
            doc['_id'] = str(doc['_id'])

        json_data = json_util.loads(json_util.dumps(documents))

        return JsonResponse({"message": json_data}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["GET"])
@token_required
def contact_requests(request):
    try:
    
        data = json.loads(request.body)

        status = request.GET.get('status', None)
        user2Id = request.GET.get('user2Id', None)
        
        if status not in ["VALIDATED", "DECLINED", "PENDING"]:
            return JsonResponse({"error": "Invalid status"}, status=400)
        
        contacts = contacts_collection.find({
            'status': status,
            'user2Id': user2Id
        })

        documents = [doc for doc in list(contacts)]

        for doc in documents:
            doc['_id'] = str(doc['_id'])

        json_data = json_util.loads(json_util.dumps(documents))

        return JsonResponse({"data": json_data}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["DELETE"])
@token_required
def remove_contact(request,contactId):
    try:
        filter = {'_id': ObjectId(contactId)}
        
        contact = contact_manager.find_by_id(contactId)
        contact['_id'] = str(contact['_id'])
        
        contacts_collection.delete_one(filter)

        return JsonResponse({"data": contact }, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["PATCH"])
@token_required
def block_contact(request, contactId):
    try:
        data = json.loads(request.body)
        action = data['action']
        isBlocked = data['isBlocked']
        user = "user1Blocked"
        
        if action == "BLOCK_CONTACT":
            filter = {'_id': ObjectId(contactId)}
        
            contact = contact_manager.find_by_id(contactId)

            if contact['user1Id'] == auth_user_id(request):
                user = "user2Blocked"
            else:
                user = "user1Blocked"

            update = {'$set': { user: isBlocked}}
            contacts_collection.update_one(filter, update)

            contact = contact_manager.find_by_id(contactId)
            contact['_id'] = str(contact['_id'])

            return JsonResponse({"data": contact }, status=200)
        else: 
            return JsonResponse({"error": 'invalid action'}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
