from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("viewlisting/<int:product_id>", views.viewlisting, name="viewlisting"),
    path("logout", views.logout_view, name="logout"),
    path("addcomment/<int:product_id>", views.addcomment, name="addcomment"),
    path("closebid/<int:product_id>", views.closebid, name="closebid"),
    path("updatewatchlist/<int:product_id>",views.updatewatchlist, name="updatewatchlist"),
    path("register", views.register, name="register"),
    path("closedlisting", views.closedlisting, name="closedlisting"),
    path("category/<str:categ>", views.category, name="category"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("createlisting",views.createlisting,name="createlisting")
]
