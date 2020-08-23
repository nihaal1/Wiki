from django.shortcuts import render
from django import forms
from django.http import HttpResponse,HttpResponseRedirect,Http404  
from django.urls import reverse
import random
import markdown2

from . import util


class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    
    content = forms.CharField(label = "Md Content",widget=forms.Textarea())

class Edit(forms.Form):
    content = forms.CharField(label = "Md Content",widget=forms.Textarea())

class Search(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class' : 'myfieldclass', 'placeholder': 'Search Encyclopedia'}))




def index(request):
    entries = util.list_entries()
    search_list = []

    if request.method == "POST":
        search = Search(request.POST)
        if search.is_valid():
            title = search.cleaned_data["title"]
            title = title.capitalize()

            for entry in entries:
                if title == entry:
                    page = util.get_entry(title)
                    html = markdown2.markdown(page)

                    return render(request, "encyclopedia/get.html",{
                        "title" : title,
                        "html" : html,
                        "search" : Search()
                    })
                    
                if title.lower() in entry.lower():
                    search_list.append(entry)
                    

            return render (request, "encyclopedia/search.html",{
                    "search_list" : search_list,
                    "search" : Search()
                    })
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search" : Search()

    })

def create(request):
    
    if request.method == "POST":
        page = NewPageForm(request.POST)
        if page.is_valid():
            
            title = page.cleaned_data["title"]
            title = title.capitalize()
            content = page.cleaned_data["content"]

            entries = util.list_entries()
            for entry in entries:
                if title == entry:
                    return HttpResponse("Error - Page exists")
                
            else:
                util.save_entry(title,content)
                return HttpResponseRedirect(f"wiki/{title}")
        
        else:
            return HttpResponse("Error")
        
    return render(request,"encyclopedia/create.html",{
        "page" : NewPageForm(),
        "search" : Search()

    })
    



def edit(request,name):

    if request.method == "GET":
        content = util.get_entry(f"{name}")
          


        return render(request, "encyclopedia/edit.html",{ 
        "content" : Edit(initial = {'content': content}),
        "search" : Search()       
        
        })

    if request.method == "POST":
        page = Edit(request.POST)
        if page.is_valid():
            title = f"{name}"
            content = page.cleaned_data["content"]
            util.save_entry(title,content)

            text = util.get_entry(title)
            html = markdown2.markdown(text)

            return render(request, "encyclopedia/get.html",{
                "title" : name,
                "html" : html,
                "search" : Search()
        })




def pages(request,name):

    try:
        text = util.get_entry(f"{name}")

        html = markdown2.markdown(text)

        return render(request, "encyclopedia/get.html",{
            "title" : name,
            "html" : html,
            "search" : Search()
        })

    except:
        
        return render(request,"encyclopedia/error_repeat.html",{
            "name" : name.capitalize(),
            "search" : Search()
        })


def random_page(request):
    if request.method == "GET":
        entries = util.list_entries()

        n= random.randint(0,len(entries)-1)
        random_page = entries[n]

        text = util.get_entry(random_page)

        html = markdown2.markdown(text)
        
    return render(request,"encyclopedia/get.html",{
            "title" : random_page,
            "html" : html,
            "search" : Search()
        })   


    
