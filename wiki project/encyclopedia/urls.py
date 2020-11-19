from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.entry,name="entry"),
    path("search",views.search,name="search"),
    path("random",views.random_pg,name="random_pg"),
    path("create",views.create,name="create"),
    path("edit",views.edit,name="edit")
]
