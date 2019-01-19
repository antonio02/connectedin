from django.shortcuts import render
from django.http import HttpResponse
from profiles.models import Profile
from .models import Post
from .forms import PostForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)
        posts = Post.objects.filter(Q(profile__user=request.user) | 
        Q(profile__contacts__user=request.user),
         ~Q(profile__blocked_contacts__user=request.user) ,
         ~Q(profile__in=user_profile.blocked_contacts.all())
        ).order_by('-post_date').all()
        return render(request, 'timeline.html', {'post_form': PostForm(),
                        'posts': posts})
    return render(request, 'timeline.html')

@login_required
def new_post(request):
    if request.method == 'POST':
        post_text = request.POST.get('post_text', None) 
        if post_text:
            user_profile = Profile.objects.get(user=request.user)
            Post.objects.create(profile=user_profile, post_text=post_text)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=400)

@login_required
def delete_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id, profile__user=request.user)
        post.delete()
        return HttpResponse(status=200)
    except Post.DoesNotExist:
        return HttpResponse(status=404)
    

