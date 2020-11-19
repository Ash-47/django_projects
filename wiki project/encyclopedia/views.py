from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
import markdown2
from . import util
from random import randint

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,title):
    if title in util.list_entries():
        return render(request,"encyclopedia/entry.html",{"title":title,"body":markdown2.markdown(util.get_entry(title))})

    else:
        raise Http404("The requested page was not found")

def search(request):
    sr=request.GET["q"]
    if sr.upper() in [x.upper() for x in util.list_entries()]:
        return render(request,"encyclopedia/entry.html",{"title":sr.capitalize(),"body":markdown2.markdown(util.get_entry(sr.capitalize()))})
    elif len(list(filter(lambda x: sr.upper() in x.upper(),util.list_entries())))>0:
        return render(request,"encyclopedia/results.html",{"results":list(filter(lambda x: sr.upper() in x.upper(),util.list_entries()))})
    else:
        return HttpResponse("<h1>No results found</h1>")

def random_pg(request):
    return redirect("entry",title=util.list_entries()[randint(0,len(util.list_entries())-1)])


def create(request):
    if request.method=="GET":
        return render(request,"encyclopedia/create.html")
    else:
        if request.POST["title"] in util.list_entries():
            return HttpResponse("<h1>This page already exists!</h1>")
        else:
            util.save_entry(request.POST['title'],request.POST['content'])
            return redirect("entry",title=request.POST['title'])

def edit(request):
        if request.method=="GET":
            return render(request,"encyclopedia/edit.html",{"title":request.GET['title'],"contents":util.get_entry(request.GET['title'])})
        else:
            util.save_entry(request.POST['title'],request.POST['content'])
            return redirect("entry",title=request.POST['title'])
