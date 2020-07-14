from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.forms import ModelForm, Textarea
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class User(AbstractUser):
    pass


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    starting_bid = models.PositiveIntegerField()
    created_dtm = models.DateTimeField(default=timezone.now, blank=False)
    image = models.URLField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_listings")
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True)
    active = models.BooleanField(default=True)

    @property 
    def current_price(self):
        try:
            return self.bids.latest('timestamp').amount
        except:
            return self.starting_bid
    @property
    def current_winner(self):
        try:
            return self.bids.latest('timestamp').user_id
        except:
            return self.user_id

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image', 'category_id']
        labels = {
            'title': _('Title'),
            'description': _('Description'),
            'starting_bid': _('Starting Bid'),
            'image': _('Image URL'),
            'category_id':_('Select Category')
        }
        widgets = {
            'description': Textarea(attrs={'cols': 30, 'rows': 10}),
        }

class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Listing,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.listing_id} by {self.user_id}"


class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_bids")
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.PositiveIntegerField()
    timestamp = models.DateTimeField(default=timezone.now, blank=False)


    def __str__(self):
        return f"{self.amount} by {self.user_id}"         


class Comment(models.Model):
    id = models.AutoField(primary_key = True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Comment_User")
    listing_id = models.ForeignKey(Listing,on_delete=models.CASCADE)
    comment = models.CharField(max_length=512)
    timestamp = models.DateTimeField(default=timezone.now, blank=False)

    def __str__(self):
        return f"{self.comment} by {self.user_id}"

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        labels = {
            'comment': _('Add Comment')
        }
        widgets = {
            'comment': Textarea(attrs={'cols': 30, 'rows': 5}),
        }
