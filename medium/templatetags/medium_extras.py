from django import template
from medium.models import UserProfile
register = template.Library()


@register.filter
def already_followed_user(author_pk, user):
    author = UserProfile.objects.get(user=author_pk)
    return author in user.profile.following.all()


@register.filter
def already_followed_topic(tag, user):
    for topic in user.profile.followed_topics_as_list():
        if tag == topic:
            return True
    return False
