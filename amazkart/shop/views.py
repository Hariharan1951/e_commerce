from django.shortcuts import render, redirect
from django.views.generic import (View, TemplateView,
                                  ListView, DetailView, 
                                  CreateView, DeleteView, 
                                  UpdateView)
from shop import models
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from shop.forms import CustomUserForm # Importing `CustomUserForm` class from forms.py 
from django.contrib.auth import authenticate, login, logout
import json

# Create your views here.

"""
This is `Class Based View` for `index.html`.

class Home(TemplateView):
    template_name = "shop/index.html"
"""
def home(request):
    products = models.Product.objects.filter(trending=1)
    return render(request, "shop/index.html",{"products":products})
    
def login_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            name = request.POST.get("username") # It gets `name=username` from `login.html` file's `User Name label` and store in `name` variable.
            pwd = request.POST.get("password")  # It gets `name=password` from `login.html` file's `Password label` and store in `pwd` variable.
            user = authenticate(request, username=name, password=pwd)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in Successfully")
                return redirect("home")
            else:
                messages.error(request, "Invalid User Name or Password")
                return redirect("login")
        return render(request, "login.html")
    

def logout_page(request):
    if request.user.is_authenticated: # It checks whether the user is already logged in. If condition satisfies means the user is already logged in, so we have to logout.
        logout(request)
        messages.success(request, "Logged out Successfully!")
    return redirect("home")
    
    
def register(request):
    form = CustomUserForm() # `CustomUserForm` class is seet to `form` variable.
    if request.method == "POST": # It check the request.method=="POST" and executes when user press `Submit Button` (or) `Register Button` from register.html page.
        form = CustomUserForm(request.POST) # passing `request.POST` as parameter in `CustomUserForm` Class after pressing `register button`.
        if form.is_valid(): # It validate the form.
            form.save()
            messages.success(request,"Registration Success!! You can LogIn Now..!")
            return redirect("login")
    return render(request, "shop/register.html",{"form":form})


"""
class Collections(ListView): 
    model = models.Category
    template_name = "shop/collections.html"
    
* From line 26 to 28 is `Class Based View` for collections.html file and we replace this with `Function Based Views` from line 35 to 37 with addition
of filter i.e. queryset in it.
"""
    
    
def collections(request):
    category = models.Category.objects.filter(status=0)
    return render(request, "shop/collections.html", {"category":category})
    
    
def collectionsview(request, name):
    if (models.Category.objects.filter(name=name, status=0)):
        products = models.Product.objects.filter(category__name=name)
        return render(request, "shop/collections_view.html",{"products":products, "category_name":name})
    else:
        messages.warning(request, "No such Category Found")
        return redirect("collections")
        
        
def product_details(request, cname, pname): # These two paramter are comes from/related to `collections_view.html` as `category_name` and `item.name`. This `cname` and `pname` are relation with to `shop.urls.py` file.
    if (models.Category.objects.filter(name=cname, status=0)): # it checks whether the given `category name` is present in `Category table`. 
        if (models.Product.objects.filter(name=pname, status=0)): # it checks whether the given `product name` is present in `Product table`.
            products = models.Product.objects.filter(name=pname, status=0).first() # the Product objects are store in the `products` varible.
            return render(request, "shop/product_details.html", {"products":products})
        else:
            messages.error(request, "No Such Product Found")
            return redirect("collectionsview")
    else:
        messages.error(request, "No Such Category Found")
        return redirect("collections")
    
    
def add_to_cart(request):
    if request.headers.get("x-requested-with")=="XMLHttpRequest":    # It checks whether we get a request from `product_details.html` using `HttpRequest` or not.
        if request.user.is_authenticated:
            data = json.load(request)
            product_qty = data["product_qty"] 
            product_id = data["pid"] # `pid` is variable which is used in `product_details.html` file.
            #print(request.user.id)
            product_status = models.Product.objects.get(id=product_id) # get the `id` of the product from models.py using `get` method.
            if product_status: # It checks the given `id` is present in product database.
                if models.Cart.objects.filter(user=request.user.id, product_id=product_id): # It checks whether that product is already exist in that user's cart.
                    return JsonResponse({"status": "Product Already in Cart"}, status=200)
                else:
                    if product_status.quantity >= product_qty:
                        models.Cart.objects.create(user=request.user, product_id=product_id, product_qty=product_qty) #  It uses `models.py Cart Class` to create.
                        return JsonResponse({"status": "Product Added to cart"}, status=200)
                    else:
                        return JsonResponse({"status": "Product Stock Not Availble"}, status=200)
        else:
            return JsonResponse({"status": "Login to Add Cart"}, status=200)
    else:
        return JsonResponse({"status": "Invalid Access"}, status=200)
        
        
def cart_page(request):
    if request.user.is_authenticated:
        cart = models.Cart.objects.filter(user=request.user)
        return render(request, "shop/cart.html", {"cart":cart})
    else:
        return redirect("home")
        

def remove_cart(request, cid):  #This `cid` is in relation with to `shop.urls.py` file.
    cart_item = models.Cart.objects.get(id=cid)
    cart_item.delete()
    return redirect("cart")
    
def remove_wish_list(request, fid):
    fav_item = models.Favourite.objects.get(id=fid)
    fav_item.delete()
    return redirect("wish_list_page")
    

def wish_list(request):
    if request.headers.get("x-requested-with")=="XMLHttpRequest":    # It checks whether we get a request from `product_details.html` using `HttpRequest` or not.
        if request.user.is_authenticated:
            data = json.load(request)
            product_id = data["pid"]
            product_status = models.Product.objects.get(id=product_id)
            if product_status:
                if models.Favourite.objects.filter(user=request.user.id, product_id=product_id):
                    return JsonResponse({"status": "Product Already in your Wish List"}, status=200)
                else:
                    models.Favourite.objects.create(user=request.user, product_id=product_id)
                    return JsonResponse({"status":"Product Added to Wish List"}, status=200)
        else:
            return JsonResponse({"status": "Login to Add Wish List"}, status=200)
    else:
        return JsonResponse({"status": "Invalid Access"}, status=200)
    
def wish_list_page(request):
    if request.user.is_authenticated:
        fav = models.Favourite.objects.filter(user=request.user)
        return render(request, "shop/wish_list_page.html", {"fav":fav})
    else:
        return redirect("login")