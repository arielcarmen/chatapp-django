from django.shortcuts import render
from .models import contacts_collection
from django.http import HttpResponse
import json
from .models import contacts_collection, DBContactManager
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from decorators import token_required

contact_manager = DBContactManager()


@csrf_exempt
@require_http_methods(["POST"])
@token_required
def send_request(request):
    try:
        data = json.loads(request.body)
        user2Id = data['user2Id']
        contact_manager.create_contact(user2Id= user2Id)
        return JsonResponse({"message": "status mis a jour"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def response_request():
    return None

def validated_contacts(request):
    return None

def response_request(request):
    return None

def remove_contact(request):
    return None

def block_contact(request):
    return None
