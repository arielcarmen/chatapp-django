from django.urls import path
from . import views

urlpatterns = [
    path('', view= views.create_discussion),
    # path('add/', view= views.add),
    # path('all/', view= views.get_all),
]