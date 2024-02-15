from django.urls import path
from . import views

urlpatterns = [
    path('', view= views.add_survey),
    path('<str:surveyId>', view= views.response_survey),
]