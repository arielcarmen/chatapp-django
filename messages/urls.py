from django.urls import path
from . import views

urlpatterns = [
    path('from', view= views.discussion_messages),
    path('', view= views.create_message),
    path('<str:messageId>', view= views.react_to_message),
]