from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.entry, name="entry"),
    path("wiki/<str:name>/delete", views.delete_entry, name="delete_entry"),
    path("wiki/<str:name>/edit", views.edit, name = "edit"),
    path("random", views.random_page, name="random"),
    path("search", views.search, name = "search"),
    path("create", views.create, name = "create"),
    path("<path:invalid_path>", views.not_found, name="not_found")
]
