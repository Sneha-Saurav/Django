from django.conf import settings
from django.contrib import admin
from django.urls import path
from cartapp.views import *

urlpatterns = [
    
    
    path('user/register', register_user_view),
     path('user/login', user_login_view),
      path('user/logout', logout_user_view),
     

     path('create', create_product_view),
     path('list', product_list_view),
     path('update/<int:pk>', update_product_view),
      path('p/update/<int:pk>', partial_update_product_view),
     
     path('get/<int:pk>', product_get_view),
     path('delete/<int:pk>', delete_product_view),




     path('address/create', create_address_view),
     path('address/list', address_list_view),
     path('address/update/<int:pk>', update_address_view),
      path('address/p/update/<int:pk>', partial_update_address_view),
      path('address/delete/<int:pk>', delete_address_view),
     
     
     
    
    
     
]