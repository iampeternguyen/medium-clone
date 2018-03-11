from django import template
from medium.models import UserProfile, Post
register = template.Library()


@register.filter
def already_followed_user(author_pk, user):
    author = UserProfile.objects.get(user=author_pk)
    return author in user.profile.following.all()


@register.filter
def already_followed_topic(tag, user):
    for followed in user.profile.followed_topics.all():
        print(tag)
        print(followed)
        if str(tag) == str(followed):
            return True
    return False


@register.filter
def already_cheered(post_pk, user):
    post = Post.objects.get(pk=post_pk)
    return user in post.cheers.all()
