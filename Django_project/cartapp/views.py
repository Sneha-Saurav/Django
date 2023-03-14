from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RegisterForm, Product_form
from django.contrib import messages
from .models import Products, Cart
# Create your views here.


def register_user(request):
    form = RegisterForm()
    if request.method == 'POST':
        # print(request.POST)
        # import pdb; pdb.set_trace()
        print(request.user)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(username, password)
        user.save()

    return render(request, 'register_user.html',{'form':form})


def product_create(request):
    product  = Product_form()
    if request.method  == 'POST':
        print(request.FILES)
        product  = Product_form(request.POST,request.FILES)
        if product.is_valid():
            # blog = blogform.save()
            product.save()
        print(request.POST)
    return render(request, 'product_create.html',{'form':product})

def product_list(request):
    if request.method  == 'GET':
        products = Products.objects.all()
    return render(request, 'list_product.html', {'products':products})

def add_to_cart(request, **kwargs):
        if pk:= kwargs.get('pk'):
            # print("sss")
            product = Products.objects.get(pk=pk)
            # action = request.GET.get('action')
            # # print(product.pk)
            # print(action)
            # print(request.GET)
            # if product.pk in Cart.product and 'qty' not in  request.GET:
            #     print("yes")
            #     error_msg =" already added to cart "
            # else:
            # product_qty = 0
            # cart.product_qty += 1
            # if action == 'increment':
            #     product_qty += 1
            # elif action == 'decrement':
            #     product_qty -= 1
            # print(product_qty)
            cart = Cart.objects.create(product_id=product.pk,product_qty = 1)
            cart.save()

            cart_session = request.session.get('cart', [])
            cart_items  = {'Name': cart.product.product_name, 'price':cart.product.price}
            cart_session.append(cart_items)
            request.session['cart'] = cart_session 
            print(request.session['cart'])
            # cart = request.session
        # return redirect('/cart/details')
        # cart =Cart.objects.all()
        return render(request, 'add_to_cart.html')

def list_cart(request):
    print("get cart")
    cart =Cart.objects.all()
    total_sum = sum(int(cp.product.price) * cp.product_qty  for cp in cart)
    return render(request, 'add_to_cart.html', {'cart': cart,'total_sum':total_sum })


def remove_cart(request,**kwargs):
    if pk:=kwargs.get('id'):
        cart = Cart.objects.get(id=pk)
        cart.delete()

    cart = cart =Cart.objects.all()
    return render(request, 'add_to_cart.html', {'cart': cart})





         

