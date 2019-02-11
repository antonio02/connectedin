from django.db import models
from profiles.models import Profile

# Create your models here.

class Post(models.Model):
    image       = models.ImageField(upload_to='posts', null=True, blank=True)
    profile     = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    post_text   = models.TextField()
    post_date   = models.DateTimeField(auto_now_add=True)
