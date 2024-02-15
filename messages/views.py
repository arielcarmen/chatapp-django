from django.shortcuts import render
from .models import messages_collection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from decorators import token_required
import json

@csrf_exempt
@require_http_methods(["POST"])
@token_required
def create_message(request):
    try:
        data = json.loads(request.body)
        email = data['email']

        return JsonResponse({"message": "status mis a jour"}, status=200)
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
        email = data['email']

        return JsonResponse({"message": "status mis a jour"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)