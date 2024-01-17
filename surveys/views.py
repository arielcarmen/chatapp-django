from django.shortcuts import render
from .models import surveys_collection
from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>App isrunning...<h1>")

def add(request):
    records = {
        "u1" : "u1",
        "u2" : "u2"
    }
    surveys_collection.insert_one(records)
    return HttpResponse("<h1>User added<h1>")

def get_all(request):
    surveys = surveys_collection.find()
    return surveys
