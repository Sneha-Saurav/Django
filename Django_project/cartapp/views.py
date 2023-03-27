from django.db.models import Q
from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from cartapp.forms import RegisterForm, Product_form, LoginForm, AddressForm, ChangePasswordForm, EditProfileForm,EditProfilePicForm, ChangePassword
from django.contrib import messages
from .models import Products, Address, Order, Wishlist, ProfileUser, Order_item
from Django_project.core.cart_helper import add_to_cart_helper, remove_from_cart_helper, decrement_cart
from django.contrib.auth import authenticate, login as authlogin, logout
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
# https://bbbootstrap.com/snippets/ecommerce-single-product-page-design-template-64204693

# https://stackoverflow.com/questions/38006125/how-to-implement-search-function-in-django

def home(request):
    print(request.GET)
    # search(request)
    print(request.GET)

    return render(request, 'index.html')


def search(request):
        print("yess")
        query = request.GET.get('search1')
        print(query)
        if query:
            products=Products.objects.filter(
                Q(category__icontains=query))
            print('yes2')
            return redirect('search_item')
        else:
             print("no")
             products = Products.objects.all()
        return render(request , 'similar_product.html',{'product':products})



def register_user(request):
    form = RegisterForm()
    try:
        if request.method == 'POST':
           
            print(request.user)
            form  = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Register Successfully')
    except Exception as er:
        print(er)
        messages.error(request, "Username already exists.")

    return render(request, 'register_user.html',{'form':form})

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        email = request.POST['email']
        password  = request.POST['password']
        print(email)
        print(password)
        user = authenticate(email = email, password=password)
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
            print("ssss")
            print(request.FILES)
            product  = Product_form(request.POST,request.FILES)
            if product.is_valid():
                print('save')
                product.save()
                return redirect('list_product')

            print(request.POST)
            messages.success(request,'Successfully Created')
    else:
         messages.error(request,'Dont have permission to create')
    return render(request, 'product_create.html',{'form':product})

def product_list(request):
    if request.user.is_authenticated:
        products = Products.objects.all()
        paginator = Paginator(products, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        page_obj =[]
        messages.error(request,'Please register or login yourself!!')
    return render(request, 'list_product.html', {'products':page_obj})



def product_details(request, **kwargs):
    if pk := kwargs.get('id'):
        product = Products.objects.get(id=pk)
        print(product.category)
        get_product= similar_product_helper(request,product.tag)
        print(get_product)
    return render(request, 'product_details.html', {'product':product, 'similar_product':get_product})


def product_delete(request, **kwargs):
    if pk := kwargs.get('id'):
          product = Products.objects.get(id=pk)
          product.delete()
          return redirect('list_product')
    return render(request, 'list_product')
    
    

def similar_product_helper(request, tag):
    similar_product = Products.objects.filter(tag=tag)
    return similar_product

def add_to_cart(request, **kwargs):
    if pk:= kwargs.get('pk'):
        cart =add_to_cart_helper(request, pk)
        print(cart)
        messages.success(request,'Product added to Cart!!')
    return render(request,'add_to_cart.html') and redirect('/cart/details')

def delete_item(request, **kwargs):
    if pk:= kwargs.get('id'):
        cart  = decrement_cart(request, pk)
        print(cart)
        redirect('cart/details')
        return render(request,'add_to_cart.html')


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
    user = ProfileUser.objects.get(id=request.user.id)
    print(user.profile_pic)
    return render(request,'profile.html',{'user':user})

def edit_profile(request):
    try:
        form  = EditProfileForm()
        user = ProfileUser.objects.get(id=request.user.id)
        if request.method == 'POST':
            form = EditProfileForm(request.POST, instance=user, initial={'mobile_no': user.mobile_no})
            if form.is_valid():
                form.save()
                messages.success(request,'Successfully Edited!!')
                return redirect('profile')
        else:
            form = EditProfileForm(instance=user)
    except Exception as er:
        messages.error(request, er)
    return render(request, 'edit_profile.html', {'form':form})

def edit_profile_pic(request):
    try:
        form  = EditProfilePicForm()
        print("111")
        if request.method == 'POST':
                print("yess")
                user = ProfileUser.objects.get(id=request.user.id)
                form = EditProfilePicForm(request.POST,request.FILES,instance=user)
                if form.is_valid():
                    print("done")
                    form.save()
                    messages.success(request,'Successfully Edited!!')
                    return redirect('profile')
    except Exception as er:
        messages.error(request, er)
    return render(request, 'profile_pic.html', {'form':form})


def change_passsword(request):
    form  = ChangePassword()
    if request.method == 'POST':
            user = ProfileUser.objects.get(id=request.user.id)
            form  = ChangePassword(request.POST, instance=user)
            password =request.POST.get('password')
            confirm_pass = request.POST.get('confirm_password')
            print(password)
            print(confirm_pass)
            if password == confirm_pass:
                print("yes done")
                if form.is_valid():
                    form.save()
                    messages.success(request,'Set Successfully')
            else:
                messages.error(request,'Password did not match')
    return render(request, 'change_pass.html', {'form':form})


def  add_address(request):
    form  = AddressForm()
    if request.method == 'POST':
            form = AddressForm(request.POST)
            if form.is_valid():
                shipping_address = form.cleaned_data['shipping_address']
                print(shipping_address)
                if Address.objects.filter(shipping_address=shipping_address).exists():
                    messages.error(request,"Address Already exists !!!")
                else:
                    print("save")
                    instance  = form.save(commit=False)
                    instance.user_id = request.user.id
                    instance.save()
                    messages.success(request,'Shipping Address added !!')
                    return redirect('home')
    return render(request, 'address.html', {'form':form})



def order_create(request, address_id):
    cart =request.session['cart']
    address = Address.objects.get(id=address_id) 
    # product = request.session.get('cart', {})
    total_sum = sum(int(cp['price']) * cp['quantity']  for p_id, cp in cart.items())
    # for p_id , p in cart.items():
        # total_sum = int(p['price']) * p['quantity']
    order = Order.objects.create(user_id=request.user.id, shipping_address=address,total_price=total_sum)
    print(order.pk)
    order_item(request,order.pk)
    messages.success(request , "Order Placed Successfully!!")
    del request.session['cart']


def order_item(request, order_id):
    cart =request.session['cart']
    for p_id , p in cart.items():
        total_sum = int(p['price']) * p['quantity']
        Order_item.objects.create(order_id=order_id,product_id=p['id'],item_price=total_sum)
        print("yess Done ")





def checkout(request):
    cart =request.session['cart']
    address = Address.objects.filter(user_id=request.user.id)
    total_sum = sum(int(cp['price']) * cp['quantity']  for p_id, cp in cart.items())
    if request.method  == 'POST':
        print(request.POST)
        if 'address' in request.POST:
            address = request.POST['address']
            print(address)
            order_create(request, address)
            return redirect('home')
        

        else:
            messages.error(request, "Please choose atleast one address")
    return render(request,'checkout_page.html',{'address':address, 'amount':total_sum})




def past_order(request):
    order_pas = Order.objects.filter(user_id=request.user.id)
    return render(request, 'order_past.html', {'orders_past': order_pas})


def get_order_item(request, **kwargs):
    if pk:= kwargs.get('id'):
        item  = Order_item.objects.filter(order_id=pk)
    print(item)
    return render(request, 'order_item.html', {'item': item})
       




def add_to_wishlist(request, **kwargs):
    if pk:= kwargs.get('id'):
        product = Products.objects.get(id=pk)
        if Wishlist.objects.filter(product_id=product.pk).exists():
            messages.error(request,' Item already added to wishlist !!')
        else:
            Wishlist.objects.create(user_id=request.user.id,product_id = product.pk) 
    
    return redirect('wishlist')

def get_wishlist(request):
    wishlist  = Wishlist.objects.filter(user_id = request.user.id)
    return render(request, 'wishlist.html', {'wishlist':wishlist})

def delete_to_wishlist(request,**kwargs):
     if pk:= kwargs.get('id'):
         wishlist = Wishlist.objects.get(id=pk)
         wishlist.delete()
         return redirect('List_cart')
     return render(request, 'wishlist.html', {'wishlist':wishlist})

    
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
                user = ProfileUser.objects.get(id=pk)
                print(user)
                user.set_password(password)
            
                user.save()
                messages.success(request,'Set Successfully')
        else:
            messages.error(request,'Password did not match')
    return render(request, 'change_pass.html', {'form':form})



    






         

