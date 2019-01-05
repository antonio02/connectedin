from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_of_birth   = models.DateField(null=False, blank=False)
    contacts        = models.ManyToManyField('Profile')
