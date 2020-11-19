from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt


def index(request):
    posts=Post.objects.all()
    posts=posts.order_by("-timestamp").all()
    for post in posts:
        post.likes=post.liked_by.all().count()
        post.save()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html",{"page_obj":page_obj})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required(login_url="/login")
def manage_likes(request,id):
    getpost=Post.objects.get(pk=id)
    if request.user in getpost.liked_by.all():
        getpost.liked_by.remove(request.user)

    else:
        getpost.liked_by.add(request.user)


    return JsonResponse({"likes":getpost.liked_by.all().count()})


@login_required
def following(request):
    flwing=request.user.following.all()
    posts=Post.objects.none()
    if flwing.count()>0:
        for user in flwing:
            posts|= Post.objects.filter(post_creator=user)


    posts=posts.order_by("-timestamp").all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    #print()
    return render(request,"network/index.html",{"page_obj":page_obj})


@login_required(login_url="/login")
def profile(request,username):
    user=User.objects.get(username=username)
    posts=Post.objects.filter(post_creator=user)
    posts=posts.order_by("-timestamp").all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,"network/profile.html",{"user_profile":user,"page_obj":page_obj})

@login_required(login_url="/login")
def manage_follow(request,id):
    user=User.objects.get(pk=id)
    req_user=User.objects.get(username=request.user.username)
    if request.user in user.followers.all():
        user.followers.remove(request.user)
        req_user.following.remove(user)
    else:
        user.followers.add(request.user)
        req_user.following.add(user)
    return JsonResponse({"followers":user.followers.all().count()})


@login_required(login_url="/login")
def new_post(request):
    if request.method=="POST":
        new_post=Post.objects.create(post_creator=request.user,post_content=request.POST.get("content"))
        return HttpResponseRedirect(reverse("index"))
    return render(request,"network/newpost.html")

@csrf_exempt
@login_required(login_url="/login")
def edit_post(request,id):
    getpost=Post.objects.get(pk=id)
    if request.method=="POST":
        data=json.loads(request.body)
        getpost.post_content=data.get("content")
        getpost.save()
        return JsonResponse({"updated_post":getpost.post_content})
#    return render(request,"network/editpost.html",{"contents":getpost})
