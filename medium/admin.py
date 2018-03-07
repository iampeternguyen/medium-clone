from django.contrib import admin
from .models import User, UserProfile, Post
from mediumeditor.admin import MediumEditorAdmin
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Post)
