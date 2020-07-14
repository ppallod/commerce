from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from .models import User, Category, Listing, Watchlist, Bid, Comment, ListingForm, CommentForm
from .utils import BidForm

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all().filter(active=True)
    })

def inactive(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all().filter(active=False)
    })

@login_required
def watchlist(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all().filter(id__in=Watchlist.objects.values_list('listing_id').filter(user_id=int(request.user.id)))
    })

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

@login_required
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

@login_required
def createlisting(request):
    if request.method == "GET":
        return render(request, 'auctions/createlisting.html', {
            'form': ListingForm()
        })
    
    if request.method == "POST":
        form = ListingForm(request.POST)
        form.instance.user_id = request.user
        if form.is_valid():
            print('Form is Valid')
            form.save()
        else:
            return render(request, 'auctions/createlisting.html', {
                'form':form
            })
        return render(request, 'auctions/status.html',{
            'heading':'Success',
            'message': 'Listing Created'
        })

@login_required
def categories(request):
    return render(request, 'auctions/categories.html',{
        'categories': Category.objects.all()
    })

@login_required
def category(request, name):
    category_name = name
    category = Category.objects.filter(name=category_name).first()
    listings = Listing.objects.all().filter(category_id=category)
    return render(request, 'auctions/index.html', {
        "listings": Listing.objects.all().filter(active=True).filter(category_id=category)
    })

def listing(request, id):
    if request.method == "GET":
        li = Listing.objects.get(pk=id)
        bids = Bid.objects.all().filter(listing_id=id).order_by('-amount', '-timestamp')
        comments = Comment.objects.all().filter(listing_id=id).order_by('-timestamp')

        if request.user.id == None:
            watchlist = close = None
        else:
            watchlist = Watchlist.objects.filter(user_id=int(request.user.id)).filter(listing_id=id).first()
            close = Listing.objects.filter(pk=id).filter(active=True).filter(user_id=request.user).first()
        
        if li.active == False:
            bidform = commentform = None
        else:
            bidform = BidForm(current_price = li.current_price)
            commentform = CommentForm()

        return render(request, 'auctions/listing.html', {
            'listing':li,
            'bids':bids,
            'comments':comments,
            'watchlist':watchlist,
            'close': close,
            'bidform':bidform,
            'commentform': commentform
        })
    
    if request.method=="POST":
        new_bid = int(request.POST['amount'])
        li = Listing.objects.get(pk=id)
        if new_bid > li.current_price:
            bid = Bid.objects.create(user_id=request.user, listing_id = li, amount=new_bid)
            bid.save()
        return HttpResponseRedirect(reverse('listing', args=(li.id,)))
    
@login_required
def addwatchlist(request, id):
    W = Watchlist.objects.create(user_id=request.user, listing_id=Listing.objects.get(pk=id))
    W.save()
    return HttpResponseRedirect(reverse("listing", args=(id,)))

@login_required
def removewatchlist(request, id):
    W = Watchlist.objects.filter(user_id=int(request.user.id)).filter(listing_id=id).filter()
    W.delete()
    return HttpResponseRedirect(reverse("listing", args=(id,)))

@login_required
def closelisting(request, id):
    listing = Listing.objects.filter(pk=id).filter(user_id=request.user).first()
    if listing is not None:
        listing.active = False
        listing.save()
        return render(request, "auctions/status.html", {
        'heading':'Success',
        'message': "Listing Closed. Highest bidder will be the winner."
    })
    else:
        return render(request, "auctions/status.html", {
            'heading':'Error',
            'message': "Unauthorized to Delete this Listing."
        })

@login_required
def addcomment(request, id):
    if request.method=="POST":
        li = Listing.objects.get(pk=id)
        form = CommentForm(request.POST)
        form.instance.user_id = request.user
        form.instance.listing_id = li
        if form.is_valid():
            form.save()
        
        return HttpResponseRedirect(reverse("listing", args=(id,)))
    
    else:
        return HttpResponseNotFound("Page Not Found")

