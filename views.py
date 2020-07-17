from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

#tasks = [] This is a global list, so anyone from any session can access it

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
    #priority = forms.IntegerField(label= "Priority", min_value=1, max_value=5)

# Create your views here.

def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []
    return render(request, "tasks/index.html", {
       # "tasks" : tasks ##The variable tasks can no longer be used as it is commented out
       "tasks" : request.session["tasks"]
    })
 
def add(request):
    if request.method =="POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            #tasks.append(task)
            request.session["tasks"] += [task]
            return HttpResponseRedirect(reverse("tasks:index")) ##DO NOT put space b/w "tasks" and :
        else:
            return render(request, "tasks/add.html", {
                "form": form
            })

    return render(request,"tasks/add.html", {
        "form" : NewTaskForm()
    })
    
