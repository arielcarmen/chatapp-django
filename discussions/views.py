from django.shortcuts import render
from .models import discussions_collection
from django.http import HttpResponse
import json
from django.http import JsonResponse
from .models import discussions_collection
from .models import DBDiscussionManager

discussion_manager = DBDiscussionManager()

# Create your views here.
def index(request):
    return HttpResponse("<h1>App isrunning...<h1>")



def get_all(request):
    discussions = discussions_collection.find()
    return discussions