from django.urls import path
from . import views

urlpatterns = [
    path('login/', view= views.login),
    path('register/', view= views.register),
    path('online/', view= views.online),
    path('reset_password/', view= views.reset_password),
]