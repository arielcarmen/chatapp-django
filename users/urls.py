from django.urls import path
from . import views

urlpatterns = [
    path('login', view= views.login),
    path('register', view= views.register),
    path('online', view= views.online),
    path('patch_password', view= views.reset_password),
    path('search', view= views.search_users),
    path('', view= views.retrieve_infos),
    path('update', view= views.update),
]