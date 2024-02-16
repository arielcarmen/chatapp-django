import jwt
import os
from django.http import JsonResponse
from functools import wraps



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
