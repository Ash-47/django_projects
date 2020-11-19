
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("like/<int:id>",views.manage_likes,name="likes"),
    path("following",views.following,name="following"),
    path("u/<username>",views.profile,name="profile"),
    path("follow/<int:id>",views.manage_follow,name="follow"),
    path("newpost",views.new_post,name="newpost"),
    path("edit/<int:id>",views.edit_post,name="edit")
]
