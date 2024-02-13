from django.urls import path
from . import views

urlpatterns = [
    path('', view= views.index),
    path('api/login/', view= views.login),
    path('api/register/', view= views.register),
    path('api/online/', view= views.online),
    path('api/reset_password/', view= views.reset_password),
]