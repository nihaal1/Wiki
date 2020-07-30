from django.shortcuts import render
from django import forms
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
import markdown2

from . import util


class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    
    content = forms.CharField(label = "Md Content",widget=forms.Textarea)



def home(request):
    return render(request, "encyclopedia/home.html")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        
    })

def create(request):
    #title = "Flask" 
    #content = "#Flask"

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
                #return HttpResponseRedirect(reverse("wiki:index"))
        
        else:
            return HttpResponse("Error")
        
    return render(request,"encyclopedia/create.html",{
        "page" : NewPageForm()
    })
    
# "util.save_entry(title,content)") 



'''
    else:
        return render(request, "encyclopedia/create.html")



def pages(request,name):
    return render(request,f"{name}.html" )
'''


def pages(request,name):
    text = util.get_entry(f"{name}")

    html = markdown2.markdown(text)
    html_file = open(f"C://Users//USER//edX Lectures//2020//Projects//wiki//encyclopedia//templates//{name}.html","w")
    html_file.write(html)
    html_file.close()
    return render(request,f"{name}.html")





    
