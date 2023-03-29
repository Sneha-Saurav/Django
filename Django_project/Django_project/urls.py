"""Django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from UserApi.views import blog_create,get_blogs, blog_edit, blog_delete, user_create, home_blog, get_blog, blog_login, publish_blog, get_published_blog, logout_user_blog, update_user, user_profile, BlogFormView, BlogView
# from cartapp.views import register_user, product_create,product_list,add_to_cart, remove_cart, list_cart , login , logout_user_product , home, login, add_address,  checkout, order_create, past_order, add_to_wishlist, get_wishlist, delete_item, delete_to_wishlist, product_details, product_delete, edit_profile, change_passsword, edit_profile_pic, search,get_order_item, blog_list
from django.conf.urls.static import static 
from cartapp.views import create_product_view


urlpatterns = [

    # Rest API
    path("products/", include("cartapp.urls")),
    # path('products/create', create_product_view),


    # path('product/list', blog_list),
    ######################################################################################################
    path('admin/', admin.site.urls),
    # path('add/blog',BlogFormView.as_view(), name='add-blog'),
    # # path('blog/<int:id>',BlogView.as_view(), name='blog-id'),
    # path('blog/', BlogView.as_view(), name='class'),
    # path('blog/get/<int:id>', get_blog, name='get_blog'),
    # path('form',solve)
    # path('', home, name='home'),
    # path('home',home_blog,name='home_blog' ),
    # path('blog/create', blog_create, name='create_blogs'),
    # path('blog/list',get_blogs , name='get_blogs'),
    # path('blog/<int:pk>/edit', blog_edit, name='edit_blogs'),
    # path('blog/<int:pk>/delete', blog_delete, name='delete_blogs'),
    # path('register/create', register_user, name='register_users'),
    # path('publish/blog/<int:id>', publish_blog, name='publish'),
    # path('published/blog/list', get_published_blog, name='published'),
    # path('user/blog/login', blog_login, name='blog_Login_user'),
    # path('user/blog/logout', logout_user_blog, name='blog_logout'),
    # path('profile/change_password/<int:id>', update_user, name='update_password'),

    # #########################################################################################################


    #   path('user/profile', user_profile, name='profile'),
    #   path('edit/profile',edit_profile, name='edit_profile'),
    #   path('edit/pic', edit_profile_pic , name='pic'),
    #    path('profile/change_password', change_passsword, name='update_password'),


    # path('product/create',product_create, name='create_product'),
    # path('product/list',product_list , name='list_product'),
    # path('product/detail/<int:id>', product_details, name='product_details'),
    #  path('product/delete /<int:id>', product_delete, name='product_delete'),

    # path('add_to_cart/<int:pk>', add_to_cart , name='add_to_cart'),
    # path('remove_from_cart/<int:id>',remove_cart, name='remove_from_cart'),
    # path('cart/details', list_cart, name='List_cart'),

    # path('user/login', login, name='Login_user'),
    # path('user/logout',logout_user_product,name='Logout_user' ),
    # path('register',register_user, name='register-user'),

    # path('login', login , name='login'),

    # path('shipping_details', add_address , name='address'),
    # path('checkout',checkout, name='checkout'),
 
    #   path('order', order_create, name='order'),
    # path('order/details',past_order, name='order-details'),

    # path('wishlist/<int:id>',add_to_wishlist, name='add-wishlist'),
    # path('wishlist/list',get_wishlist, name='wishlist'),
    # path('/delete/wishlist/<int:id>',delete_to_wishlist, name='delete-wishlist'),
    # path('delete/item/<int:id>',delete_item, name='decrement'),

    # path('order/item/<int:id>',get_order_item, name='order_item'),


    
    # path('search/result',search, name='search_item'),

    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
