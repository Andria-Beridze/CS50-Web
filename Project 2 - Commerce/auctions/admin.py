from django.contrib import admin
from .models import *

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "price", "user", "date"]
    filter_horizontal = ["category"]
    
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "listing"]
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "category"]
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "listing", "user", "comment", "comment_date"]

admin.site.register(User)

admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Watchlist, WatchlistAdmin)