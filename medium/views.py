from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils import timezone
from itertools import chain
import re

from medium.forms import (UserForm, UserProfileForm, PostForm,
                          UserEditForm, PostFeaturedImageForm, CommentForm)
from medium.models import Post, UserProfile, Comment, Topic
# Create your views here.


class IndexView(generic.ListView):
    template_name = 'medium/index.html'
    context_object_name = 'posts_list'

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:10]

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a Queryset

        if self.request.user.is_authenticated and self.request.user.profile:
            followed_topics = self.request.user.profile.followed_topics.all()
            followed_users = self.request.user.profile.following.all()
            q_objects = Q()
            for topic in followed_topics:
                q_objects.add(Q(tags__name=topic), Q.OR)

            for user in followed_users:
                q_objects.add(Q(author=user.user), Q.OR)

            context['followed_posts'] = Post.objects.filter(
                q_objects).distinct().order_by(('-published_date'))

        return context

# TODO FIX THIS VIEW


class TagsListView(generic.ListView):
    template_name = 'medium/topic_list.html'
    context_object_name = 'posts_list'

    def get_queryset(self):
        return Post.objects.filter(tags__name__in=[self.kwargs['tag']])

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet
        context['tag'] = self.kwargs['tag']
        return context


class NewPostView(LoginRequiredMixin, generic.CreateView):
    login_url = '/login/'
    redirect_field_name = 'medium/post.html'
    template_name = 'medium/new_post.html'
    form_class = PostForm
    model = Post

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    login_url = '/login/'
    model = Post
    success_url = reverse_lazy('medium:index')


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'medium/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


class PostEditView(LoginRequiredMixin, generic.UpdateView):
    login_url = '/login/'
    redirect_field_name = 'medium/post.html'
    template_name = 'medium/new_post.html'
    form_class = PostForm
    model = Post


def add_comment(request, pk):
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = Post.objects.get(pk=pk)
            comment.author = request.user
            comment.save()
    return HttpResponseRedirect(reverse('medium:post', kwargs={'pk': pk}))


def register_user(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        user_profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and user_profile_form.is_valid():
            new_user = user_form.save()
            new_user.set_password(new_user.password)
            new_user.save()

            new_user_profile = user_profile_form.save(commit=False)
            new_user_profile.user = new_user

            if 'avatar' in request.FILES:
                new_user_profile.avatar = request.FILES['avatar']

            new_user_profile.save()
            registered = True
        else:
            print(user_form.errors, user_profile_form.errors)
    else:
        user_form = UserForm()
        user_profile_form = UserProfileForm()
    return render(request, 'medium/registration.html', {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
        'registered': registered
    })


def new_post(request):

    if request.method == 'POST':
        post_form = PostForm(data=request.POST)
        post_featured_image_form = PostFeaturedImageForm(data=request.POST)
        if post_form.is_valid() and post_featured_image_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()

            if 'featured_image' in request.FILES:

                post.avatar = request.FILES['featured_image']
                post.save()

    else:
        post_form = PostForm()
        post_featured_image_form = PostFeaturedImageForm()

    return render(request, 'medium/new_post.html', {
        'form': post_form,
        'featured_form': post_featured_image_form,

    })


def search_posts(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        posts_list = Post.objects.filter(Q(published_date__lte=timezone.now()),
                                         Q(title__contains=search) | Q(content__contains=search)).order_by('-published_date')[:10]

        return render(request, 'medium/index.html', {'posts_list': posts_list})
    else:
        return HttpResponseRedirect(reverse('medium:index'))


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('medium:index'))
        else:
            return HttpResponse('invalid login details')
    else:
        return render(request, 'medium/login.html')


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return HttpResponseRedirect(reverse('medium:post', kwargs={'pk': pk}))


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('medium:index'))


@login_required
def profile_edit(request):

    if request.method == 'POST':
        user_form = UserForm(data=request.POST, instance=request.user)
        user_profile_form = UserProfileForm(
            data=request.POST, instance=request.user.profile)

        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            user_profile = user_profile_form.save(commit=False)
            user_profile.user = user

            if 'avatar' in request.FILES:
                user_profile.avatar = request.FILES['avatar']

            user_profile.save()

    user_form = UserEditForm(instance=request.user)
    user_profile_form = UserProfileForm(instance=request.user.profile)
    return render(request, 'medium/profile_edit.html', {
        'user_profile_form': user_profile_form,
        'user_form': user_form,
    })


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('medium:post', pk=post_pk)


@login_required
def follow_user(request, author_pk, post_pk):
    user = UserProfile.objects.get(user=request.user)
    print(user)
    # user.followed_users += str(author) + ','
    follow = UserProfile.objects.get(user=author_pk)
    print(follow)
    user.following.add(follow)
    user.save()
    return redirect('medium:post', pk=post_pk)
    # followed_users += user + ', '


@login_required
def unfollow_user(request, author_pk, post_pk):
    user = UserProfile.objects.get(user=request.user)
    print(user)
    # user.followed_users += str(author) + ','
    follow = UserProfile.objects.get(user=author_pk)
    print(follow)
    user.following.remove(follow)
    user.save()
    return redirect('medium:post', pk=post_pk)
    # followed_users += user + ', '


@login_required
def follow_topic(request, tag):
    user = UserProfile.objects.get(user=request.user)
    user.followed_topics.add(tag)
    user.save()
    return redirect('medium:tags', tag=tag)


@login_required
def unfollow_topic(request, tag):
    user = UserProfile.objects.get(user=request.user)
    user.followed_topics.remove(tag)
    user.save()
    return redirect('medium:tags', tag=tag)
