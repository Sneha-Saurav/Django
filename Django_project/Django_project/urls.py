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
from UserApi.views import blog_create,get_blogs, blog_edit, blog_delete, user_create
from cartapp.views import register_user, product_create,product_list,add_to_cart
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', csrf_exempt(index)),
    # path('blog/<int:blog_id>', get_blog),
    # path('form',solve)
    path('blog/create', blog_create),
    path('blog/list',get_blogs ),
    path('blog/<int:pk>/edit', blog_edit),
    path('blog/<int:pk>/delete', blog_delete),
    path('user/create', register_user),
    path('product/create',product_create),
    path('product/list',product_list),
    path('add_to_cart/<int:pk>', add_to_cart)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
