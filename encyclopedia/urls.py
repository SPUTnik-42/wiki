from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("add_entry", views.new_entry, name="add_entry"),
    path("search", views.search, name="search"),
    path("random_page", views.random_page, name="random_page"),
    path("wiki/edit_page/<str:entry>", views.edit_page, name="edit_page")
]
