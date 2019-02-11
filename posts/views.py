from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from profiles.models import Profile
from .models import Post
from .forms import PostForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)
        posts = Post.objects.filter(Q(profile__user=request.user) | 
        Q(profile__contacts__user=request.user),
         ~Q(profile__blocked_contacts__user=request.user),
         ~Q(profile__in=user_profile.blocked_contacts.all()),
         ~Q(profile__user__is_active=False)
        ).order_by('-post_date').all()

        paginador = Paginator(posts, 10)
        page = request.GET.get('page')
        posts = paginador.get_page(page)

        contacts = user_profile.contacts.filter(
            ~Q(user__in=[i.user for i in user_profile.blocked_contacts.all()]),
            user__is_active=True).all()
        return render(request, 'timeline.html',
                      {'post_form': PostForm(),
                       'user_profile': user_profile,
                       'posts': posts,
                       'received_invitations': user_profile.received_invitations.filter(
                           sender__user__is_active=True).all(),
                       'sent_invitations': user_profile.sent_invitations.filter(
                           receiver__user__is_active=True).all(),
                       'contacts': contacts},)
    return render(request, 'timeline.html')

@login_required
def admin_timeline(request):
    if not request.user.is_superuser:
        return HttpResponse(status=404)
    user_profile = Profile.objects.get(user=request.user)
    contacts = user_profile.contacts.all()
    all_profiles = Profile.objects.exclude(Q(user=request.user) |
                                           Q(user__in=[i.user for i in contacts]) |
                                           Q(received_invitations__sender=user_profile) |
                                           Q(sent_invitations__receiver=user_profile)).all()

    paginador = Paginator(all_profiles, 10)
    page = request.GET.get('page')
    all_profiles = paginador.get_page(page)

    return render(request, 'admin_timeline.html',
                  {'all_profiles': all_profiles,
                   'contacts': contacts,
                   'user_profile': user_profile,
                   'received_invitations': user_profile.received_invitations.all(),
                   'sent_invitations': user_profile.sent_invitations.all()})

@login_required
def new_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            user_profile = Profile.objects.get(user=request.user)
            post = post_form.save(commit=False)
            post.profile = user_profile
            post.save()
            messages.success(request, _('Post created successfully'))
            return redirect('index')
        else:
            messages.error(request, _('Invalid data for new post'))
            return redirect('index')
    else:
        messages.error(request, _('Method not allowed'))
        return redirect('index')

@login_required
def delete_post(request, post_id):
    try:
        if request.user.is_superuser:
            post = Post.objects.get(id=post_id)
        else:
            post = Post.objects.get(id=post_id, profile__user=request.user)
        post.delete()
        messages.success(request, _('Post deleted successfully'))
        return HttpResponse(status=200)
    except Post.DoesNotExist:
        messages.error(request, _('Post not found'))
        return HttpResponse(status=404)

@login_required
def like_post(request, post_id):
    try:
        if request.user.is_superuser:
            post = Post.objects.get(id=post_id)
        else:
            post = Post.objects.get(id=post_id, profile__user=request.user)

        user_profile = Profile.objects.get(user=request.user)
        if user_profile in post.likes.all():
            messages.warning(request, _('You already liked this post'))
            return HttpResponse(status=400)
        else:
            post.likes.add(user_profile)
            messages.success(request, _('Post liked'))
            return HttpResponse(status=200)
    except Post.DoesNotExist:
        messages.error(request, _('Post not found'))
        return HttpResponse(status=404)

@login_required
def dislike_post(request, post_id):
    try:
        if request.user.is_superuser:
            post = Post.objects.get(id=post_id)
        else:
            post = Post.objects.get(id=post_id, profile__user=request.user)

        user_profile = Profile.objects.get(user=request.user)
        if user_profile in post.likes.all():
            post.likes.remove(user_profile)
            messages.warning(request, _('Post disliked'))
            return HttpResponse(status=200)
        else:
            messages.warning(request, _('You did not like this post'))
            return HttpResponse(status=400)
    except Post.DoesNotExist:
        messages.error(request, _('Post not found'))
        return HttpResponse(status=404)
    

