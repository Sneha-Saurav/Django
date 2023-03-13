from django.shortcuts import render
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
            product = Products.objects.get(pk=pk)
            print(product.pk)
            cart = Cart.objects.create(product_id=product.pk, product_qty=1)
            cart.save()
        cart =Cart.objects.all()
        return render(request, 'add_to_cart.html', {'cart': cart})





         

