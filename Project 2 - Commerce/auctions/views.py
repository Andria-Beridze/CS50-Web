from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.filter(active = True).order_by("title"),
        "watchlist_count": watchlist_count(request)
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password.",
                "watchlist_count": watchlist_count(request)
            })
    else:
        return render(request, "auctions/login.html", {
            "watchlist_count": watchlist_count(request)
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match.",
                "watchlist_count": watchlist_count(request)
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
                "watchlist_count": watchlist_count(request)
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html", {
            "watchlist_count": watchlist_count(request)
        })

def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        url = request.POST["url"]
        categories = request.POST.getlist("categories")
        
        new_listing = Listing(title = title, description = description, price = price, image_url = url, user = request.user)
        new_listing.save()
        
        for category in categories:
            new_listing.category.add(Category.objects.get(category = category))
        
        return HttpResponseRedirect(reverse("index"))
        
        
    return render(request, "auctions/create.html", {
        "categories": Category.objects.all().order_by("category"),
        "watchlist_count": watchlist_count(request)
    })
    
def listing(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(pk = id)
        price = request.POST["bid_value"]
        
        if float(price) <= listing.price:
            return render(request, "auctions/listing.html", {
                "listing": Listing.objects.get(pk = id),
                "isUnderWatchlist": request.user.is_authenticated and Watchlist.objects.filter(user = request.user, listing = Listing.objects.get(pk = id)).exists(),
                "bid_count": Bid.objects.filter(listing = Listing.objects.get(pk = id)).count(),
                "message": "Your bid must be higher than the current amount",
                "success": False,
                "comments": Comment.objects.filter(listing = Listing.objects.get(pk = id)),
                "watchlist_count": watchlist_count(request)
            })
        else:
            listing.price = float(price)
            listing.winner = request.user
            
            listing.save()
            
            new_bid = Bid(user = request.user, bid = float(price), listing = listing)
            new_bid.save()
            
            return render(request, "auctions/listing.html", {
                "listing": Listing.objects.get(pk = id),
                "isUnderWatchlist": request.user.is_authenticated and Watchlist.objects.filter(user = request.user, listing = Listing.objects.get(pk = id)).exists(),
                "bid_count": Bid.objects.filter(listing = Listing.objects.get(pk = id)).count(),
                "message": "Your bid as successfully received",
                "success": True,
                "comments": Comment.objects.filter(listing = Listing.objects.get(pk = id)),
                "watchlist_count": watchlist_count(request)
            })
    
    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(pk = id),
        "isUnderWatchlist": request.user.is_authenticated and Watchlist.objects.filter(user = request.user, listing = Listing.objects.get(pk = id)).exists(),
        "bid_count": Bid.objects.filter(listing = Listing.objects.get(pk = id)).count(),
        "comments": Comment.objects.filter(listing = Listing.objects.get(pk = id)),
        "watchlist_count": watchlist_count(request)
    })
    
def toggleWatchlist(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("listing", args = (id, )))
    
    if Watchlist.objects.filter(user = request.user, listing = Listing.objects.get(pk = id)).exists():
        wl = Watchlist.objects.get(user = request.user, listing = Listing.objects.get(pk = id))
        wl.delete()
    
    else:
        wl = Watchlist(user = request.user, listing = Listing.objects.get(pk = id))
        wl.save()
    
    return HttpResponseRedirect(reverse("listing", args = (id, )))

def close(request, id):
    listing = Listing.objects.get(pk = id)
    if request.user == listing.user:
        listing.active = False
        listing.save()
    
    return HttpResponseRedirect(reverse("listing", args = (id, )))

def closed_listings(request):
    return render(request, "auctions/closed.html",{
        "listings": Listing.objects.filter(active = False).order_by("title"),
        "watchlist_count": watchlist_count(request)
    })
    
def comment(request, id):
    if request.method == "POST":
        comment = request.POST["comment"]
        
        new_comment = Comment(user = request.user, comment = comment, listing = Listing.objects.get(pk = id))
        new_comment.save()
    
    return HttpResponseRedirect(reverse("listing", args = (id, )))

def watchlist(request):
    if request. user.is_authenticated:
        return render(request, "auctions/watchlist.html", {
            "list": Watchlist.objects.filter(user = request.user),
            "watchlist_count": watchlist_count(request)
        })
    else:
        return render(request, "auctions/watchlist.html", {
            "watchlist_count": watchlist_count(request)
        })
    
def watchlist_count(request):
    if request.user.is_authenticated:
        return Watchlist.objects.filter(user = request.user).count()
    else:
        return 0
        
def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all().order_by("category"),
        "watchlist_count": watchlist_count(request)
    })
    
def specific_category(request, name):
    return render(request, "auctions/specific_category.html", {
        "listings": Listing.objects.filter(category = Category.objects.get(category = name), active=True),
        "watchlist_count": watchlist_count(request),
        "name": name
    })