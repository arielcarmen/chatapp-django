from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from werkzeug.security import generate_password_hash
from .models import users_collection
from django.http import HttpResponse
from .models import DBUserManager
import json
from datetime import timedelta, datetime
import jwt
from decorators import token_required
import os


user_manager = DBUserManager()
SECRET_KEY = os.environ.get('DJANGO_JWT_SECRET_KEY', 'votre_cle_secrete_par_defaut')


@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    try:
        data = json.loads(request.body)
        firstname = data['firstname']
        lastname = data['lastname']
        email = data['email']
        password = data['password']
        result = user_manager.create_user(lastname, firstname, email, password)
        user = users_collection.find_one(result.inserted_id)
        user['_id'] = str(user['_id'])
        return JsonResponse({"data": user}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    try:
        data = json.loads(request.body)
        email = data['email']
        password = data['password']
        if user_manager.check_password(email, password):
            user = user_manager.find_user_by_email(email= email)
            payload = {
                'user_id': str(user['_id']),
                'email': email,
                'exp': datetime.utcnow() + timedelta(days=100),  # Le token expire après 100 jour
                'iat': datetime.utcnow()
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

            user = user_manager.find_user_by_email(email= email)
            user['_id'] = str(user['_id'])
            user.pop('password', None)

            return JsonResponse({"token":token, "user": user}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials."}, status=401)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
@token_required
def online(request):
    try:
        data = json.loads(request.body)
        email = data['email']
        users_collection.update_one({'email': email}, {'$set': {'status': 'En ligne'}})

        return JsonResponse({"message": "status mis a jour"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    


@csrf_exempt
@require_http_methods(["POST"])
@token_required
def reset_password(request):
    try:
        data = json.loads(request.body)
        email = data['email']
        old_password = data['currentPassword']
        new_password = data['newPassword']

        user = user_manager.find_user_by_email(email= email)

        if user_manager.check_password(email, old_password):
            hashed_password = generate_password_hash(new_password)
            users_collection.update_one({'email': email}, {'$set': {'password': hashed_password}})
            payload = {
                'email': email,
                'exp': datetime.utcnow() + timedelta(days=100),  # Le token expire après 100 jour
                'iat': datetime.utcnow()
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

            return JsonResponse({"message": "Mot de passe mis a jour","token":token}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials."}, status=401)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    

@csrf_exempt
@require_http_methods(["POST"])
@token_required
def method(request):
    try:
        data = json.loads(request.body)
        email = data['email']

        return JsonResponse({"message": "status mis a jour"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)