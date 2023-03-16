from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from cartapp.forms import RegisterForm, Product_form, LoginForm
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
        email  =  request.POST.get('email')
        user = User.objects.create_user(username, password =password, email=email)
        user.save()
        messages.success(request,'Register Successfully')

    return render(request, 'register_user.html',{'form':form})

def login(request):
    form = LoginForm()
    username = request.POST.get('username')
    password = request.POST.get("password")
    user = authenticate(request,username=username, password=password)
    print(user)
    if user is not None:
        authlogin(request,user)
        messages.success(request,'Login Successfully')
        
    else:
        print("error")
        messages.error(request, 'Invalid Credentials')
    return render(request, 'login.html', {'form': form})


def logout_user(request):
    logout(request)
    print(request.user)
    return redirect('/product/list')


def product_create(request):
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
            messages.success(request,'Successfully Created')
    else:
         messages.error(request,'Dont have permission to create')
    return render(request, 'product_create.html',{'form':product})

def product_list(request):
    if request.user.is_authenticated:
        if request.method  == 'GET':
            products = Products.objects.all()
    else:
        products =[]
        messages.error(request,'Please register or login yourself!!')
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
    
    if 'cart' in request.session:
        cart =request.session['cart']
        print(cart)
        total_sum = sum(int(cp['price']) * cp['quantity']  for cp_id , cp in cart.items())
    else:
         messages.error(request,'Cart sn empty!!')
         cart ={}
         total_sum = 0

    return render(request, 'add_to_cart.html', {'cart': cart , 'total_sum':total_sum}) 


def home(request):
    return render(request, 'index.html')





         

