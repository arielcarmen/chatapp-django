from django.shortcuts import render
from .models import messages_collection
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("<h1>App isrunning...<h1>")

def add(request):
    records = {
        "u1" : "u1",
        "u2" : "u2"
    }
    messages_collection.insert_one(records)
    return HttpResponse("<h1>User added<h1>")

def get_all(request):
    messages = messages_collection.find()
    return messages