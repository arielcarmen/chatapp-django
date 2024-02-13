import jwt
import os
from django.http import JsonResponse
from functools import wraps



SECRET_KEY = os.environ.get('DJANGO_JWT_SECRET_KEY', 'votre_cle_secrete_par_defaut')

def token_required(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        token = None

        # Récupérer le token de l'en-tête de la requête
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Supposer que le token est préfixé par "Bearer "

        # Si le token est manquant, retourner une erreur 401 (non autorisé)
        if not token:
            return JsonResponse({'message': 'Token is missing!'}, status=401)

        try:
            # Décoder le token JWT
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            # Vous pouvez ajouter ici une étape pour récupérer l'utilisateur à partir de la base de données si nécessaire
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'Token has expired!'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'message': 'Invalid token!'}, status=401)

        # Si tout est bon, continuer vers la vue originale
        return f(request, *args, **kwargs)

    return decorated_function

# Utiliser le décorateur sur une vue
@token_required
def some_protected_view(request):
    # Vue qui nécessite une authentification
    pass
