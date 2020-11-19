from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *


def index(request):
    products=Listing.objects.all()
    categories=Categories.objects.all()
    return render(request, "auctions/index.html", {"products": products,"categories":categories})


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



def viewlisting(request,product_id):

    categories=Categories.objects.all()
    comments = Comment.objects.filter(comm_id=product_id)
    if request.method == "POST":
        item = Listing.objects.get(id=product_id)
        newbid = int(request.POST.get('newbid'))
        # checking if the newbid is greater than or equal to current bid
        if item.bid.bid_value >= newbid:
            return render(request, "auctions/viewlisting.html", {
                "product": item,
                "message": "Your bid should be greater than the existing bid value!",
                "msg_type": "danger",
                "comments": comments,
                "categories":categories
            })
        
        else:
            b=Bid.objects.get(bid_item=item)
            b.bid_value = newbid
            b.user=request.user.username
            b.save()
            

            product = Listing.objects.get(id=product_id)
            return render(request, "auctions/viewlisting.html", {
                "product": product,
                "message": "Your Bid is added.",
                "msg_type": "success",
                "comments": comments,
                "categories":categories
            })
    
    else:
        product = Listing.objects.get(id=product_id)
        return render(request, "auctions/viewlisting.html", {
            "product": product,
            "added": len(Watchlist.objects.filter(item=product,user=request.user.username))!=0,
            "comments": comments,
            "categories":categories
        })


@login_required(login_url='/login')
def addcomment(request, product_id):
    categories=Categories.objects.all()
    obj = Comment()
    obj.comm_id=Listing.objects.get(pk=product_id)
    obj.user = request.user.username
    obj.comment = request.POST.get("comment")
    obj.save()
    # returning the updated content
    print("displaying comments")
    comments = Comment.objects.filter(comm_id=product_id)
    product = Listing.objects.get(id=product_id)

    return render(request, "auctions/viewlisting.html", {
        "product": product,
        "added": len(Watchlist.objects.filter(item=product,user=request.user.username))!=0,
        "comments": comments,
        "categories":categories
    })


@login_required(login_url='/login')
def closebid(request, product_id):
    categories=Categories.objects.all()
    listobj = Listing.objects.get(id=product_id)
    winobj = Winner()
    winobj.user=listobj.bid.user
    winobj.seller=listobj.user
    winobj.title=listobj.title
    winobj.final_bid=listobj.bid.bid_value
    winobj.save()
    
    listobj.delete()
   
    winners = Winner.objects.all()
    return render(request, "auctions/closedlisting.html", {
        "products": winners,
        "message": "Bid Closed",
        "msg_type": "success",
        "categories":categories
    })


@login_required(login_url='/login')
def updatewatchlist(request, product_id):

    obj=None
    try:
        obj = Watchlist.objects.get(item=product_id, user=request.user.username)
    except:
        pass
    comments = Comment.objects.filter(comm_id=product_id)
    categories=Categories.objects.all()
   
    if obj:
     
        obj.item.remove(Listing.objects.get(id=product_id))
  
        product = Listing.objects.get(id=product_id)
    
        return render(request, "auctions/viewlisting.html", {
            "product": product,
            "added": False,
            "comments": comments,
            "message":"Removed from your watchlist",
            "msg_type":"danger",
            "categories":categories
        })
    else:
       
        try:
            obj = Watchlist.objects.get(user=request.user.username)
        except:
            pass
        if obj:
            obj.item.add(Listing.objects.get(id=product_id))
        else:
            w=Watchlist()
            w.user=request.user.username
            w.save()
            w.item.add(Listing.objects.get(pk=product_id))
       
        product = Listing.objects.get(id=product_id)
      
        return render(request, "auctions/viewlisting.html", {
            "product": product,
            "added": True,
            "comments": comments,
            "message":"Added to your watchlist",
            "msg_type":"success",
            "categories":categories
        })


@login_required(login_url='/login')
def closedlisting(request):
    
    winners = Winner.objects.all()
 

    return render(request, "auctions/closedlisting.html", {
        "products": winners
    })


def category(request, categ):
  
    c=Categories.objects.get(category_name=categ)
    categ_products = Listing.objects.filter(category=c)
    categories=Categories.objects.all()
    return render(request, "auctions/category.html", {
        "categ": categ,
        "products": categ_products,
        "categories":categories
    })


@login_required(login_url="/login")
def watchlist(request):
    w=None
    categories=Categories.objects.all()
    try:
        w=Watchlist.objects.get(user=request.user.username)
    except:
        pass
    if w:
        products=Listing.objects.filter(watchlist=w)
    else:
        products=None
    return render(request,"auctions/watchlist.html",{"products":products,"categories":categories})


@login_required(login_url='/login')
def createlisting(request):
    categories=Categories.objects.all()
    
    if request.method == "POST":
        
        item = Listing()
       
        item.user = request.user.username
        item.title = request.POST.get('title')
        item.desc= request.POST.get('description')
        item.category=Categories.objects.get(category_name=request.POST.get('category'))
        item.img_link = request.POST.get('img_link')
        item.save()
        bid=Bid()
        bid.bid_item =item
        bid.user=item.user
        bid.bid_value=int(request.POST.get('bid_value'))
        bid.save()
        
        products = Listing.objects.all()
        return render(request, "auctions/index.html", {
            "products": products,
            "categories": categories
        })
  
    else:
        return render(request, "auctions/createlisting.html",{"categories":categories})
