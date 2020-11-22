from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/page/new", views.new_page, name="new_page"),
    path("wiki/<str:entry_name>/edit", views.edit_page, name="edit_page"),
    path("wiki/<str:entry_name>", views.entry, name="entry"),
    path("random_entry", views.random_entry, name="random_entry"),
    path("wiki/search/result", views.search_results, name="search_results"),
    # path("wiki/new", views.new_page, name="new_page")
]
