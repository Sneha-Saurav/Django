from django.contrib import admin
from UserApi.models import Blog
from django.utils import timezone


# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title','author','description','is_published','create_date','is_recently_published']
    # list_filter =['is_published']
    # search_fields=['title']

    def is_recently_published(self, obj):
         if obj.is_published == True:
            var = obj.create_date
            now_time = timezone.now()
            blog_end_time = now_time + timezone.timedelta(days=2) #tommorow
            blog_start_time = now_time - timezone.timedelta(days=2) #yesterday
            if  var > blog_start_time and var < blog_end_time:
                return True
            else:
                return False
admin.site.register(Blog, BlogAdmin)
