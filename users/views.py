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
from bson import ObjectId
from utils import auth_user_id

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
        errors = []

        if users_collection.find_one({"email": email}):
            errors.append("Cet e-mail est déjà utilisé.")

        if not any(char.isupper() for char in password):
            errors.append("Le mot de passe doit contenir au moins une majuscule.")

        if not any(char.islower() for char in password):
            errors.append("Le mot de passe doit contenir au moins une minuscule.")

        if not any(char.isdigit() for char in password):
            errors.append("Le mot de passe doit contenir au moins un chiffre.")

        if not any(char in r"@#$%_&!*?" for char in password):
            errors.append("Le mot de passe doit contenir au moins un caractère spécial (@#$%&!*?).")

        if len(password) < 8:
            errors.append("Le mot de passe doit faire au moins 8 caractères de long.")

        if errors:
            return JsonResponse({"error": errors}, status=400)
        
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
        user = user_manager.find_user_by_email(email)
        user['_id'] = str(user['_id'])
        user.pop('password', None)

        return JsonResponse({"data": user}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["PATCH"])
@token_required
def update(request):
    try:
        data = json.loads(request.body)
        firstname = data['firstname']
        lastname = data['lastname']
        email = data['email']
        photoUrl = data['photoUrl']
        users_collection.update_one({'_id': ObjectId(auth_user_id)}, 
        {'$set': {'firstname': firstname, 'lastname': lastname, 'photoUrl': photoUrl, 'status': 'En ligne'}}
            )
        user = user_manager.find_user_by_email(email)
        user['_id'] = str(user['_id'])
        user.pop('password', None)

        return JsonResponse({"data": user}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["GET"])
@token_required
def retrieve_infos(request):
    try:
        data = json.loads(request.body)
        token = data['token']

        token_data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        
        user_id = token_data['user_id']
        
        user = user_manager.find_by_id(user_id)
        user['_id'] = str(user['_id'])
        user.pop('password', None)

        return JsonResponse({"token": token, "user": user}, status=200)
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
        user["_id"] = str(user["_id"])

        if user_manager.check_password(email, old_password):
            hashed_password = generate_password_hash(new_password)
            users_collection.update_one({'email': email}, {'$set': {'password': hashed_password}})
            payload = {
                'user_id': str(user['_id']),
                'email': email,
                'exp': datetime.utcnow() + timedelta(days=100),  # token valide 100jours
                'iat': datetime.utcnow()
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            user.pop('password', None)

            return JsonResponse({"token":token,"data": user}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials."}, status=401)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    

@csrf_exempt
@require_http_methods(["GET"])
@token_required
def search_users(request):
    try:
        data = json.loads(request.body)
        text = data['text']

        users = list(users_collection.find({
            "$or": [
                {"lastname": {"$regex": text, "$options": "i"}},
                {"firstname": {"$regex": text, "$options": "i"}},
                {"email": {"$regex": text, "$options": "i"}}
            ]
        }).limit(20).skip(0))

        for user in users:
            user["_id"] = str(user["_id"])

        return JsonResponse({"data": users}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)