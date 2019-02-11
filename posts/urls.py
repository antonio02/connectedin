from django.urls import path
from .views import new_post, delete_post, like_post, dislike_post, comment_post

urlpatterns = [
    path('new/', new_post, name='new_post'),
    path('<int:post_id>/delete/', delete_post, name='delete_post'),
    path('<int:post_id>/like/', like_post, name='like_post'),
    path('<int:post_id>/dislike/', dislike_post, name='dislike_post'),
    path('<int:post_id>/comment/', comment_post, name='comment_post'),
]