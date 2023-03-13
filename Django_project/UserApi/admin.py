from django.contrib import admin
from UserApi.models import Blog
from django.utils import timezone


# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title','author','description','is_published','create_date','is_recently_published']
    # list_filter =['is_published']
    # search_fields=['title']

    def is_recently_published(self, obj):
            published_date = obj.create_date
            current =  timezone.now()
            end_date = current + timezone.timedelta(days=1) # date of tommorow
            start_date = current - timezone.timedelta(days=1) # date of yesterday
            if start_date <= published_date <= end_date:
                return True
            else:
                return False
    is_recently_published.short_description ='Recent Published'
admin.site.register(Blog, BlogAdmin)
