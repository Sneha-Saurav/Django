from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RegisterForm, Product_form
from django.contrib import messages
from .models import Products
from Django_project.core.cart_helper import add_to_cart_helper, remove_from_cart_helper
from django.contrib.auth import authenticate, login as authlogin, logout


def register_user(request):
    form = RegisterForm()
    if request.method == 'POST':
        # print(request.POST)
        # import pdb; pdb.set_trace()
        print(request.user)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(username, password =password)
        user.save()

    return render(request, 'register_user.html',{'form':form})

def login(request):
    error= ""
    form = RegisterForm()
    username = request.POST.get('username')
    password = request.POST.get("password")
    user = authenticate(request,username=username, password=password)
    print(user)
    if user is not None:
        authlogin(request,user)
        print("loginned!!")
        
    else:
        print("error")
        error = 'Invalid Credentials'
    return render(request, 'login.html', {'form': form})


def logout_user(request):
    logout(request)
    print(request.user)
    return redirect('/product/list')


def product_create(request):
    error = " "
    product  = Product_form()
    if request.user.is_authenticated and request.user.has_perm('cartapp.add_products'):
        print(request.user.has_perm('cartapp.add_products'))
        print(request.user.is_authenticated)
        if request.method  == 'POST':
            print(request.FILES)
            product  = Product_form(request.POST,request.FILES)
            if product.is_valid():
                product.save()
            print(request.POST)
    else:
        error = "Dont have permission to create "
    return render(request, 'product_create.html',{'form':product, 'msg':error})

def product_list(request):
    if request.user.is_authenticated:
        if request.method  == 'GET':
            products = Products.objects.all()
    return render(request, 'list_product.html', {'products':products})


def add_to_cart(request, **kwargs):
    if pk:= kwargs.get('pk'):
        cart =add_to_cart_helper(request, pk)
        print(cart)
        redirect('cart/detail')
    return render(request,'add_to_cart.html') and redirect('/cart/details')



def remove_cart(request,**kwargs):
    if pk:=kwargs.get('id'):
       cart_delete =remove_from_cart_helper(request, pk)
       print(cart_delete)
    return render(request, 'add_to_cart.html') and redirect('/cart/details')


def list_cart(request):
    print("get cart")
    cart =request.session['cart']
    print(cart)
    total_sum = sum(int(cp['price']) * cp['quantity']  for cp_id , cp in cart.items())
    return render(request, 'add_to_cart.html', {'cart': cart , 'total_sum':total_sum}) 





         

