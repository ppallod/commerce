from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("inactive", views.inactive, name="inactive"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("categories", views.categories, name="categories"),
    path("category/<str:name>", views.category, name="category"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("addwatchlist/<int:id>", views.addwatchlist, name="addwatchlist"),
    path("removewatchlist/<int:id>", views.removewatchlist, name="removewatchlist"),
    path("closelisting/<int:id>", views.closelisting, name="closelisting"),
    path("addcomment/<int:id>", views.addcomment, name="addcomment")
]
