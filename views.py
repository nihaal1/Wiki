from django.shortcuts import render

from . import util

def home(request):
    return render(request, "encyclopedia/home.html")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        
    })

def get(request,name):
    return render(request,f"{name}.html" )