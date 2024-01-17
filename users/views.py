from django.shortcuts import render
from .models import users_collection
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("<h1>App isrunning...<h1>")

def add(request):
    records = {
        "u1" : "u1",
        "u2" : "u2"
    }
    users_collection.insert_one(records)
    return HttpResponse("<h1>User added<h1>")

def get_all(request):
    users = users_collection.find()
    return users
