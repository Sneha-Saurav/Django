from django.db.models import Q
from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from cartapp.forms import RegisterForm, Product_form, LoginForm, AddressForm, ChangePasswordForm, EditProfileForm,EditProfilePicForm, ChangePassword
from django.contrib import messages
from .models import Products, Address, Order, Wishlist, ProfileUser, Order_item
from Django_project.core.cart_helper import add_to_cart_helper, remove_from_cart_helper, decrement_cart
from django.contrib.auth import authenticate, login as authlogin, logout
from django.core.paginator import Paginator
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.views import generic
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
# from django.views.generic import ListView
# from django.views.generic.detail import DetailView


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class AddressFilter(django_filters.FilterSet):

    user__username = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Address
        fields =['user']

        
class AddressViewset(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AddressFilter





class CreateUserSerializer(ModelSerializer):
    class Meta:
        model = ProfileUser
        exclude = ('last_login','is_superuser','is_staff','is_active','user_permissions', 'groups')
        
    def create(self, validated_data):
        u = ProfileUser.objects.create_user(**validated_data)
        return u 
       
       

class UserSerializer(ModelSerializer):
    class Meta:
        model = ProfileUser
        fields = ['id', 'username', 'email', 'last_login', 'first_name', 'last_name']
       
    




@api_view(http_method_names=('post',))
@permission_classes([IsAdminUser])
def create_product_view(request):
    serializer  = ProductSerializer(data=request.data)
    print(serializer)
    if serializer.is_valid():
        serializer.save()
    return Response({'Product':serializer.data}, status=status.HTTP_201_CREATED)


@api_view()
def product_list_view(request):
    p = Products.objects.all()
    return Response({'Product':ProductSerializer(p,many=True).data})



@api_view()
def product_get_view(request, pk):
    p = Products.objects.get(id=pk)
    return Response({'Product':ProductSerializer(p).data})


@api_view(http_method_names=('patch',))
@permission_classes([IsAdminUser])
def partial_update_product_view(request, pk):
    product = Products.objects.get(id=pk)
    serializer = ProductSerializer(product, data = request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response({'Product':serializer.data}, status=status.HTTP_200_OK)

@api_view(http_method_names=('put',))
@permission_classes([IsAdminUser])
def update_product_view(request, pk):
    product = Products.objects.get(id=pk)
    serializer = ProductSerializer(product, data = request.data)
    if serializer.is_valid():
        serializer.save()
    return Response({'Product':serializer.data}, status=status.HTTP_200_OK)


@api_view(http_method_names=('delete',))
def delete_product_view(request, pk):
    product = Products.objects.get(id=pk)
    product.delete()
    # serializer = ProductSerializer(product, data = request.data)
    # if serializer.is_valid():
    #     serializer.save()
    return Response({'message':"Successfully Deleted"}, status=status.HTTP_202_ACCEPTED)




@api_view(http_method_names=('post',))
@permission_classes([IsAuthenticated])
def create_address_view(request):
    print(request.user)
    request.data['user'] = request.user.id
    serializer  = AddressSerializer(data=request.data)
    try:
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
    except:
        print(serializer.errors)
        return  Response({'Address':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'Address':serializer.data}, status=status.HTTP_201_CREATED)



@api_view()
@permission_classes([IsAuthenticated])
def address_list_view(request):
    try:
        p = Address.objects.all()

    except Address.DoesNotExist:
        return Response({'Address':"Address list not found !!"})

    return Response({'Address':AddressSerializer(p,many=True).data})




@api_view(http_method_names=('put',))
@permission_classes([IsAuthenticated])
def update_address_view(request, pk):
    try:
        request.data['user'] = request.user.id
        address = Address.objects.get(id=pk, user=request.user)
        serializer = AddressSerializer(address, data = request.data)
        if serializer.is_valid():
            serializer.save()
    except Address.DoesNotExist:
        return  Response({'Message':' Address Not Found!'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'Address':serializer.data}, status=status.HTTP_200_OK)


@api_view(http_method_names=('patch',))
@permission_classes([IsAuthenticated])
def partial_update_address_view(request, pk):
    try:
        request.data['user'] = request.user.id
        address = Address.objects.get(id=pk, user_id=request.user.id)
        print(address)
        serializer = AddressSerializer(address, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
    except Address.DoesNotExist:
        return  Response({'Message':' Address Not Found!'})
    return Response({'Address':serializer.data}, status=status.HTTP_200_OK)




@api_view(http_method_names=('delete',))
@permission_classes([IsAuthenticated])
def delete_address_view(request, pk):
    try:
        address = Address.objects.get(id=pk)
        address.delete()
    except Address.DoesNotExist:
         return Response({'message':"Not Found "}, status=status.HTTP_202_ACCEPTED)

    return Response({'message':"Successfully Deleted"}, status=status.HTTP_202_ACCEPTED)


@api_view(http_method_names=('post',))
def register_user_view(request):
    serializer  = CreateUserSerializer(data=request.data)
    try:
        if serializer.is_valid():
            print("yes")
            serializer.save()
        else:
            print(serializer.errors)

    except:
        print(serializer.errors)
        return  Response({'User':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'User':serializer.data}, status=status.HTTP_201_CREATED)
    

@api_view(http_method_names=('post',))
def user_login_view(request):
    user = ProfileUser.objects.get(email=request.data['email'])
    user_match = UserSerializer(user)
    authenticate_user  = authenticate(request , email=user.email, password=request.data['password'])
    if authenticate_user is not None:
        authlogin(request, authenticate_user)
        token = Token.objects.create(user=user)
        print(token)
    else:
        print("yes")
        return Response({'message':"Invalid Credentials"})
    print(request.user.id)
    return Response({'User':user_match.data, 'Token':token.key})

@api_view()
@permission_classes([IsAuthenticated])
def logout_user_view(request):
    try:
       
        token = Token.objects.get(user_id=request.user.id)
        print(token)
        token.delete()
        logout(request)
    except:
        return Response({'message':"Try Again !!"})

    return Response({'User':"Successfully Logout"})
    















































































































#------------------------------- MVT---------------------------------------------------------------------------------------------------
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



class CreateProductView(generic.CreateView):
    form_class = Product_form
    template_name ='product_new.html'
    success_url ='/product'
    success_message = 'Product Successfully Created'



# def product_create(request):
#     product  = Product_form()
#     if request.user.is_authenticated and request.user.has_perm('cartapp.add_products'):
#         print(request.user.has_perm('cartapp.add_products'))
#         print(request.user.is_authenticated)
#         if request.method  == 'POST':
#             print("ssss")
#             print(request.FILES)
#             product  = Product_form(request.POST,request.FILES)
#             if product.is_valid():
#                 print('save')
#                 product.save()
#                 return redirect('list_product')

#             print(request.POST)
#             messages.success(request,'Successfully Created')
#     else:
#          messages.error(request,'Dont have permission to create')
#     return render(request, 'product_create.html',{'form':product})



class ProductListView(generic.ListView):
    model = Products
    context_object_name = 'product_list'
    template_name = 'product_list.html' 
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['count'] = Products.objects.count()
        return context

# def product_list(request):
#     if request.user.is_authenticated:
#         products = Products.objects.all()
#         paginator = Paginator(products, 3)
#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page(page_number)
#     else:
#         page_obj =[]
#         messages.error(request,'Please register or login yourself!!')
#     return render(request, 'list_product.html', {'products':page_obj})


class  ProductDetailView(generic.DetailView):
    model = Products
    template_name = 'product_details.html'
    context_object_name = 'product' 


# def product_details(request, **kwargs):
#     if pk := kwargs.get('id'):
#         product = Products.objects.get(id=pk)
#         print(product.category)
#         get_product= similar_product_helper(request,product.tag)
#         print(get_product)
#     return render(request, 'product_details.html', {'product':product, 'similar_product':get_product})


class ProductsUpdateView(generic.UpdateView):
    model = Products
    template_name = 'products_form.html'
    form_class = Product_form
    success_url = '/product'


class DeleteProductsView(generic.DeleteView):
    model = Products
    template_name = 'product_confirm_delete.html'
    success_url = '/product'
    success_message = 'Product Successfully Deleted'

# def product_delete(request, **kwargs):
#     if pk := kwargs.get('id'):
#           product = Products.objects.get(id=pk)
#           product.delete()
#           return redirect('list_product')
#     return render(request, 'list_product')
    
    

def similar_product_helper(request,tag):
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



    






         

