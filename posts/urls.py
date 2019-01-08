from django.urls import path
from .views import new_post, delete_post

urlpatterns = [
    path('new/', new_post, name='new_post'),
    path('<int:post_id>/delete', delete_post, name='delete_post'),
]