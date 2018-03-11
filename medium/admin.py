from django.contrib import admin
from .models import User, UserProfile, Post, Comment, Topic
from mediumeditor.admin import MediumEditorAdmin
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Topic)
