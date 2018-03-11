import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()

from faker import Faker
from medium.models import User, UserProfile, Post, Comment
import random
fake = Faker()


def fake_users(n):
    for i in range(0, n):
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = first_name + last_name
        email = fake.email()
        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        user.save()
        profile = UserProfile(user=user)
        profile.bio = fake.sentence() + ' ' + fake.sentence() + ' ' + fake.sentence()
        profile.save()


def fake_posts(n):
    total_users = User.objects.count()

    for i in range(0, n):
        random_user_index = random.randint(0, total_users - 1)

        author = User.objects.all()[random_user_index]

        title = fake.sentence()
        content = ""

        for j in range(0, 10):
            content += '<h3>' + fake.sentence() + '</h3>'
            content += '&nbsp;' * 4 + fake.sentence()
            for l in range(0, 30):
                content += fake.sentence() + ' '
            content += '<br><br>'
        created_date = fake.past_date(
            start_date="-1y", tzinfo='America/New_York')
        published_date = created_date
        post = Post(
            title=title,
            content=content,
            author=author,
            created_date=created_date,
            published_date=published_date
        )
        post.save()

        for i in range(0, 4):
            post.tags.add(fake.color_name())
        post.save()


def fake_comments(n):
    total_posts = Post.objects.count()

    total_users = User.objects.count()
    for i in range(0, n):
        random_post_index = random.randint(0, total_posts - 1)
        random_user_index = random.randint(0, total_users - 1)

        author = User.objects.all()[random_user_index]
        post = Post.objects.all()[random_post_index]

        content = ""
        for j in range(0, 5):
            content += fake.sentence() + ' '
        created_date = fake.past_date(
            start_date="-1y", tzinfo='America/New_York')
        comment = Comment(
            author=author,
            post=post,
            content=content,
            created_date=created_date
        )
        comment.save()


if __name__ == "__main__":
    fake_users(15)
    fake_posts(200)
    fake_comments(1000)
