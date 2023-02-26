# SHOP URLS.PY

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    path("cart/", views.cart_page, name="cart"),
    path("removecart/<str:cid>/", views.remove_cart, name="remove_cart"), # It receives `item.id` from `cart.html` file and store in `cid`, then sent/make relationship with `views.py` file and acts as parameter for remove_cart function . 
    path("remove_wish_list/<str:fid>/", views.remove_wish_list, name="remove_wish_list"),
    path("addtocart/", views.add_to_cart, name="addtocart"),
    path("wishlist/", views.wish_list, name="wish_list"),
    path("wishlistpage/", views.wish_list_page, name="wish_list_page"),
    path("collections/", views.collections, name="collections"),
    path("collections/<str:name>/", views.collectionsview, name="collectionsview"), # For this url, we have to pass `single parameter`.
    path("collections/<str:cname>/<str:pname>/", views.product_details, name="product_details"), # For this url, we have to pass `2 parameters`. This `cname` and `pname` are relation with to `views.py` file.
]