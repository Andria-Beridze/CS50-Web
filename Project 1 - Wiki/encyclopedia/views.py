from django.shortcuts import render
from django.http import HttpResponseRedirect
from markdown import markdown
from django.urls import reverse
import random

from . import util

entry_list = []

def index(request):
    if request.method == "POST":
        search_query = request.POST["search_query"]
        
        if util.get_entry(search_query) != None:
            return HttpResponseRedirect(reverse("entry", args = (search_query, )))
        
        else:
            entries = util.list_entries()
            global entry_list
            entry_list = []
            
            for entry in entries:
                if search_query.lower() in entry.lower():
                    entry_list.append(entry)
                
            return HttpResponseRedirect(reverse("search"))
                    
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    content = util.get_entry(name)
    
    if content != None:
        result = markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "entry": result,
            "title": name
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": name
        })
        
def not_found(request, invalid_path):
    return render(request, "encyclopedia/not_found.html")

def random_page(request):
    entries = util.list_entries()
    rand = entries[random.randint(0, len(entries) - 1)]
    
    return HttpResponseRedirect(reverse("entry", args = (rand, )))

def delete_entry(request, name):
    util.delete_entry(name)
    return HttpResponseRedirect(reverse("index"))

def search(request):
    global entry_list
    
    return render(request, "encyclopedia/search.html", {
        "search_result": entry_list
    })
    
def create(request):
    if request.method == "POST":
        form = request.POST
        
        title = form["title"]
        content = form["content"]
        
        if util.get_entry(title) != None:
            return render(request, "encyclopedia/create.html", {
                "entry_exists": True
            })
        
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", args = (title, )))
    
    return render(request, "encyclopedia/create.html", {
        "entry_exists": False
    })
    
def edit(request, name):
    if request.method == "POST":
        form = request.POST
    
        content = form["content"]
        
        util.save_entry(name, content)
        return HttpResponseRedirect(reverse("entry", args = (name, )))
    
    return render(request, "encyclopedia/edit.html", {
        "entry": util.get_entry(name),
        "title": name
    })