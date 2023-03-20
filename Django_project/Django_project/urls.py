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
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from UserApi.views import  BlogView, blog_create,get_blogs, blog_edit, blog_delete, user_create, home_blog, get_blog, blog_login, publish_blog, get_published_blog, logout_user_blog, update_user, user_profile
from cartapp.views import register_user, product_create,product_list,add_to_cart, remove_cart, list_cart , login , logout_user , home
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog', BlogView.as_view(), name='class'),
    path('blog/<int:id>', get_blog, name='get_blog'),
    # path('form',solve)
    path('', home, name='home'),
    path('home',home_blog,name='home_blog' ),
    # path('blog/create', blog_create, name='create_blogs'),
    path('blog/list',get_blogs , name='get_blogs'),
    path('blog/<int:pk>/edit', blog_edit, name='edit_blogs'),
    path('blog/<int:pk>/delete', blog_delete, name='delete_blogs'),
    path('register/create', register_user, name='register_users'),
    path('publish/blog/<int:id>', publish_blog, name='publish'),
    path('published/blog/list', get_published_blog, name='published'),
    path('user/blog/login', blog_login, name='blog_Login_user'),
    path('user/blog/logout', logout_user_blog, name='blog_logout'),
    path('user/profile', user_profile, name='profile'),
    path('profile/change_password/<int:id>', update_user, name='update_password'),


    path('product/create',product_create, name='create_product'),
    path('product/list',product_list , name='list_product'),
    path('add_to_cart/<int:pk>', add_to_cart , name='add_to_cart'),
    path('remove_from_cart/<int:id>',remove_cart, name='remove_from_cart'),
    path('cart/details', list_cart, name='List_cart'),
    path('user/login', login, name='Login_user'),
    path('user/logout',logout_user,name='Logout_user' )
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
