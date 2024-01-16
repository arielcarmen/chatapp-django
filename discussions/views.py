from django.shortcuts import render
from .models import discussions_collection
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("<h1>App running...<h1>")

def add(request):
    records = {
        "u1" : "u1",
        "u2" : "u2"
    }
    discussions_collection.insert_one(records)
    return HttpResponse("<h1>User added<h1>")

def get_all(request):
    discussions = discussions_collection.find()
    return discussions