from django.db import models
from profiles.models import Profile


# Create your models here.

class Post(models.Model):
    image = models.ImageField(upload_to='posts', null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    post_text = models.TextField(null=True, blank=True)
    post_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Profile, related_name='liked_posts')
    post_shared = models.ForeignKey('self',
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    blank=True, related_name='shares')
    is_shared_post = models.BooleanField(default=False)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-comment_date']
