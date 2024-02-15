from django.urls import path
from . import views

urlpatterns = [
    path('send_request/', view= views.send_request),
    path('contact_requests', view= views.contact_requests),
    path('response_request/<str:contactId>', view= views.response_request),
    path('validated_requests', view= views.validated_contacts),
    path('block_contact/<str:contactId>', view= views.block_contact),
    path('remove_contact/<str:contactId>', view= views.remove_contact),
]