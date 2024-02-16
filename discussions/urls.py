from django.urls import path
from . import views

urlpatterns = [
    path('', view= views.create_discussion),
    path('all', view= views.discussions),
    path('archived', view= views.archived_discussions),
    path('pinned', view= views.pinned_discussions),
    path('archived', view= views.archived_discussions),
    path('<str:discussionId>/add_member', view= views.add_user_group),
    path('<str:discussionId>/remove_member', view= views.remove_user_group),
    path('<str:discussionId>/update', view= views.update_group),
    path('<str:discussionId>/pin', view= views.pin_unpin_group),
    path('<str:discussionId>/archive', view= views.archive_unarchive_discussion),
    path('<str:discussionId>/mute', view= views.mute_unmute_discussion),
    path('<str:discussionId>/leave', view= views.leave_discussion),
    path('<str:discussionId>/delete', view= views.delete_group),
    path('<str:discussionId>', view= views.get_discussion),
]