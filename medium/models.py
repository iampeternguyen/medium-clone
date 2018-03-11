from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.db.models import Q
from django.core.paginator import Paginator

from taggit.managers import TaggableManager
from froala_editor.fields import FroalaField

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(
        upload_to='avatars', default='avatars/default-profile.png')
    followed_topics = TaggableManager(blank=True)

    following = models.ManyToManyField(
        'self', related_name='follows', symmetrical=False, blank=True)

    # def followed_topics_as_list(self):
    #     return self.followed_topics.split(',')

    # def followed_users_as_list(self):
    #     return self.followed_users.split(',')

    def recent_posts(self):
        return Post.objects.filter(author=self.user).order_by('-published_date')[:10]

    def recent_comments(self):
        return Comment.objects.filter(author=self.user).order_by('-created_date')[:10]

    def recent_cheers(self):
        return Post.objects.filter(cheers__in=[self.user])[:10]

    def followed_posts(self):
        followed_topics = self.followed_topics.all()
        followed_users = self.following.all()
        q_objects = Q()
        if followed_topics:
            for topic in followed_topics:
                print(topic)
                q_objects.add(Q(tags__name__in=topic), Q.OR)
        if followed_users:
            for user in followed_users:
                q_objects.add(Q(author=user.user), Q.OR)
        if q_objects:
            posts = Post.objects.filter(
                q_objects).distinct().order_by(('-published_date'))
        return posts

    def paginated_followed_posts(self):
        return Paginator(self.followed_posts(), 10)

    def __str__(self):
        return str(self.user)


class FeaturedImage(models.Model):
    image = models.ImageField(upload_to='posts', blank=True)


class Topic(models.Model):
    tags = models.CharField(max_length=200, blank=True, unique=True)

    def __str__(self):
        return self.tags


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,)
    title = models.CharField(max_length=200)
    content = FroalaField()
    featured_image = models.ImageField(
        upload_to='posts', blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    tags = TaggableManager(blank=True)
    cheers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="post_cheers", symmetrical=False, blank=True)

    def author_string(self):
        return str(self.author)

    def all_comments(self):
        return self.comments.all().order_by('-created_date')

    def __str__(self):
        return self.title

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('medium:post', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('post', kwargs={
            'pk': self.pk
        })
