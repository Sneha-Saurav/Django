from django.db import models

# Create your models here.
class Blog(models.Model):
    title=models.CharField(max_length=200)
    author = models.CharField(max_length=20)
    description = models.TextField()
    is_published= models.BooleanField(default=False)
    create_date = models.DateTimeField()
    class Meta:
        permissions = (
            ('can_publish', 'Can only Publish'),
            )





