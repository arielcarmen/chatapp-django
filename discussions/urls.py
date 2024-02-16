from django.urls import path
from . import views

urlpatterns = [
    path('', view= views.create_discussion),
    path('all', view= views.discussions),
    path('archived', view= views.archived_discussions),
    path('pinned', view= views.pinned_discussions),
    path('archived', view= views.archived_discussions),
    path('<str:discussionId>/add_member', view= views.add_user_group),
    # path('add/', view= views.add),
    # path('all/', view= views.get_all),
]