from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from cartapp.forms import RegisterForm, Product_form, LoginForm, AddressForm, ChangePasswordForm
from django.contrib import messages
from .models import Products, Address, Order
from Django_project.core.cart_helper import add_to_cart_helper, remove_from_cart_helper
from django.contrib.auth import authenticate, login as authlogin, logout





def home(request):
    return render(request, 'index.html')



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
        return redirect('home')
        
    else:
        print("error")
        messages.error(request, 'Invalid Credentials')
    return render(request, 'login.html', {'form': form})


def logout_user_product(request):
    logout(request)
    print(request.user)
    return redirect('home')


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
        return redirect('register-user')
    return render(request, 'list_product.html', {'products':products})


def add_to_cart(request, **kwargs):
    if pk:= kwargs.get('pk'):
        cart =add_to_cart_helper(request, pk)
        print(cart)
        messages.success(request,'Product added to Cart!!')
        redirect('cart/detail')
    return render(request,'add_to_cart.html') and redirect('/cart/details')



def remove_cart(request,**kwargs):
    if pk:=kwargs.get('id'):
       cart_delete =remove_from_cart_helper(request, pk)
       print(cart_delete)
       messages.success(request,'Product remove from Cart!!')
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

def user_profile(request):
    return render(request,'profile.html')

def  add_address(request):
    form  = AddressForm()
    # if request.method  == 'GET':
    #     address = Address.objects.get(user_id=request.user.id)

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            print("save")
            instance  = form.save(commit=False)
            instance.user_id = request.user.id
            instance.save()
            print("save")
            return redirect('home')
    return render(request, 'address.html', {'form':form})




def order_create(request,**kwargs):
    # pk= kwargs.get('id')
    cart =request.session['cart']
    address = Address.objects.get(user_id=request.user.id) 
    product = request.session.get('cart', {})
    print(product)
    total_sum = sum(int(cp['price']) * cp['quantity']  for cp_id, cp in cart.items())
    for p_id , p in cart.items():
        print(p['id'])
        order = Order.objects.create(user_id=request.user.id, shipping_address=address,total_price=total_sum, product_id=p['id'])
    return redirect('home')

def checkout(request):
    cart =request.session['cart']
    address = Address.objects.get(user_id=request.user.id)
    print(address)
    total_sum = sum(int(cp['price']) * cp['quantity']  for p_id, cp in cart.items())
    # order_create(request)
    # order = Order.objects.get(user_id=request.user.id)
    print(total_sum)
    return render(request,'checkout_page.html',{'address':address, 'amount':total_sum})

def past_order(request):
    order_pas = Order.objects.filter(user_id=request.user.id)
    print(order_pas)
    return render(request, 'order_past.html', {'orders_past': order_pas})

    
def update_user(request,**kwargs):
    form  = ChangePasswordForm()
    if request.method == 'POST':
        if pk:= kwargs.get('id'):
            password =request.POST.get('password')
            confirm_pass = request.POST.get('confirm_password')
            print(password)
            if password == confirm_pass:
                print(pk)
                print("yes done")
                user = User.objects.get(id=pk)
                print(user)
                user.set_password(password)
            
                user.save()
                messages.success(request,'Set Successfully')
        else:
            messages.error(request,'Password did not match')
    return render(request, 'change_pass.html', {'form':form})
    






         

