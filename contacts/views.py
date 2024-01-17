from django.shortcuts import render
from .models import contacts_collection
from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>App isrunning...<h1>")

def add(request):
    records = {
        "u1" : "u1",
        "u2" : "u2"
    }
    contacts_collection.insert_one(records)
    return HttpResponse("<h1>User added<h1>")

def get_all(request):
    contacts = contacts_collection.find()
    return contacts

# Create your views here.
