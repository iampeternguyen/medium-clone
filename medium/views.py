from django.shortcuts import render
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils import timezone

from medium.forms import UserForm, UserProfileForm, PostForm
from medium.models import Post
# Create your views here.


class IndexView(generic.ListView):
    template_name = 'medium/index.html'
    context_object_name = 'posts_list'

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class NewPostView(LoginRequiredMixin, generic.CreateView):
    login_url = '/login/'
    redirect_field_name = 'medium/post.html'
    template_name = 'medium/new_post.html'
    form_class = PostForm
    model = Post

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'medium/post.html'


class PostEditView(LoginRequiredMixin, generic.UpdateView):
    login_url = '/login/'
    redirect_field_name = 'medium/post.html'
    template_name = 'medium/new_post.html'
    form_class = PostForm
    model = Post


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


def search_posts(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        posts_list = Post.objects.filter(
            Q(title__contains=search) | Q(content__contains=search))
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
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('medium:index'))
