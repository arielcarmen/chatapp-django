import jwt

def auth_user_id(request):
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(' ')[1]  

    token_data = jwt.decode(token, 'votre_cle_secrete_par_defaut', algorithms=['HS256'])
    
    user_id = token_data['user_id']
    return user_id