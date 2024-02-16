import jwt
import os
from django.http import JsonResponse
from functools import wraps
from discussions.models import discussions_collection
from bson import ObjectId
from utils import auth_user_id



SECRET_KEY = os.environ.get('DJANGO_JWT_SECRET_KEY', 'votre_cle_secrete_par_defaut')

def token_required(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Supposer que le token est préfixé par "Bearer "

        if not token:
            return JsonResponse({'message': 'Token is missing!'}, status=401)

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'Token has expired!'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'message': 'Invalid token!'}, status=401)

        return f(request, *args, **kwargs)

    return decorated_function


def member_of_discussion(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        discussion_id = kwargs.get('discussion_id')
        user_id = auth_user_id(request)
        try:
            discussion = discussions_collection.find_one({"_id": ObjectId(discussion_id), "members.userId": user_id})
            if discussion:
                return func(request, *args, **kwargs)
            else:
                return JsonResponse({"error": "User is not a member of this discussion"}, status=403)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return wrapper