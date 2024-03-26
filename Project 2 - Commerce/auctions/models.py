from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length = 64)
    
    def __str__(self):
        return f"{ self.category }"

class Listing(models.Model):
    title = models.CharField(max_length = 64)
    description = models.CharField(max_length = 2048)
    price = models.DecimalField(max_digits = 10, decimal_places = 2, validators=[MinValueValidator(0)])
    
    image_url = models.URLField(null = True, blank = True)
    category = models.ManyToManyField(Category, null = True, blank = True)
    
    active = models.BooleanField(default = True)
    date = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "user")
    winner = models.ForeignKey(User, null = True, blank = True, on_delete = models.CASCADE, related_name = "winner")
    
    def __str__(self):
        return f"{ self.title }: ${ self.price }"
    
class Comment(models.Model):
    comment = models.CharField(max_length = 1024)
    listing = models.ForeignKey(Listing, null = True, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    comment_date = models.DateTimeField(auto_now_add = True, null = True)
    
    def __str__(self):
        return f"{ self.user.username } commented: { self.comment }"
    

class Bid(models.Model):
    bid = models.DecimalField(max_digits = 10, decimal_places = 2, validators=[MinValueValidator(0)])
    listing = models.ForeignKey(Listing, null = True, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    
    def __str__(self):
        return f"{ self.user.username } bade: { self.bid }"
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    listing = models.ForeignKey(Listing, null = True, on_delete = models.CASCADE)