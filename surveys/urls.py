from django.urls import path
from . import views

urlpatterns = [
    path('', view= views.index),
    path('add/', view= views.add),
    path('all/', view= views.get_all),
]