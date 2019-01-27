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
        contacts = user_profile.contacts.exclude(profile__in=user_profile.blocked_contacts.all()).all()
        return render(request, 'timeline.html',
                      {'post_form': PostForm(),
                       'posts': posts,
                       'received_invitations': user_profile.received_invitations.all(),
                       'sent_invitations': user_profile.sent_invitations.all(),
                       'contacts': contacts},)
    return render(request, 'timeline.html')

@login_required
def admin_timeline(request):
    if not request.user.is_superuser:
        return HttpResponse(status=404)
    user_profile = Profile.objects.get(user=request.user)
    contacts = user_profile.contacts.exclude(profile__in=user_profile.blocked_contacts.all()).all()
    all_profiles = Profile.objects.exclude(Q(user=request.user) |
                                           Q(user__in=[i.user for i in contacts]) |
                                           Q(received_invitations__sender=user_profile) |
                                           Q(sent_invitations__receiver=user_profile)).all()
    return render(request, 'admin_timeline.html',
                  {'all_profiles': all_profiles,
                   'contacts': contacts,
                   'user_profile': user_profile,
                   'received_invitations': user_profile.received_invitations.all(),
                   'sent_invitations': user_profile.sent_invitations.all(),})

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
    

