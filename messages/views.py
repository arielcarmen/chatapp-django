from django.shortcuts import render
from .models import messages_collection, DBMessageManager
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from decorators import token_required
import json

message_manager = DBMessageManager()

@csrf_exempt
@require_http_methods(["POST"])
@token_required
def create_message(request):
    try:
        
        discussionId = request.POST.get('discussionId', None)
        contactId = request.POST.get('contactId', None)
        respondToMsgId = request.POST.get('responseToMsgId', None)
        text = request.POST.get('text', None)
        file = request.FILES.get('file', None)
        if file:
            file_info = {
                'name': file.name,
                'content_type': file.content_type,
                'size': file.size,
                'type' : file.content_type
            }
            with open('messages/uploads/'+file.name, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
        
        result = message_manager.create_message(discussionId= discussionId, contactId= contactId, text=text, file= file_info, respondToMsgId= respondToMsgId)

        message = message_manager.find_by_id(result.inserted_id)
        message['_id'] = str(message['_id'])
        return JsonResponse({"data": message}, status=200)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["PATCH"])
@token_required
def react_to_message(request):
    try:
        data = json.loads(request.body)
        email = data['email']

        return JsonResponse({"message": "status mis a jour"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["GET"])
@token_required
def discussion_messages(request):
    try:
        data = json.loads(request.body)

        discussion_id = request.GET.get('discussionId', None)
        limit = int(request.GET.get('$limit', 20))
        sort_order = int(request.GET.get('$sort[createdAt]', -1))

        query = {"discussionId": discussion_id}
        sort = [("createdAt", sort_order)]  
        messages = list(messages_collection.find(query).sort(sort).limit(limit))

        return JsonResponse({"message": messages}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)