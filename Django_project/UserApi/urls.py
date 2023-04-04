from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from UserApi.views import *
from rest_framework.routers import DefaultRouter


# router = DefaultRouter()

# router.register(r'blog',BLogViewset, basename='blog')
# urlpatterns = router.urls



urlpatterns = [
    #  path('', include(router.urls)),
    
    path('create',BlogCreateAPIVIEW.as_view(), name='add-blog'),
    # path('blog/<int:id>',BlogView.as_view(), name='blog-id'),
    path('list', BlogListAPIVIEW.as_view(), name='class'),
    path('retreive/<int:pk>', BlogRetreiveAPIVIEW.as_view(), name='get_blog'),
    path('', BlogListCreateAPIVIEW.as_view(), name='get_blog'),
    path('<int:pk>', BlogRetrieveUpdateDestroyView.as_view(), name='get_blog'),
    path('user/list',ProfileListAPIVIEW.as_view()),
  

    



]