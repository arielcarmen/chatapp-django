from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from .models import users_collection
from django.http import HttpResponse
from .models import DBUserManager
import json
from datetime import timedelta


user_manager = DBUserManager()

def index(request):
    return HttpResponse("<h1>App isrunning...<h1>")

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    try:
        data = json.loads(request.body)
        firstname = data['firstname']
        lastname = data['lastname']
        email = data['email']
        password = data['password']
        user_manager.create_user(lastname, firstname, email, password)
        return JsonResponse({"message": "User created successfully."}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    try:
        data = json.loads(request.body)
        firstname = data['firstname']
        lastname = data['lastname']
        password = data['password']
        if user_manager.check_password(lastname, firstname, password):
            # Vous devriez ici créer un token de session ou JWT
            return JsonResponse({"message": "Login successful."}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials."}, status=401)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
