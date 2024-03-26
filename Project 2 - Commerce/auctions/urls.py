from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listings/<int:id>", views.listing, name="listing"),
    path("listings/<int:id>/watchlist", views.toggleWatchlist, name="toggle_watchlist"),
    path("listings/<int:id>/close", views.close, name="close"),
    path("listings/closed", views.closed_listings, name="closed_listings"),
    path("listings/<int:id>/comment", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:name>", views.specific_category, name="specific_category")
]
