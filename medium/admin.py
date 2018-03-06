from django.contrib import admin
from .models import User, UserProfile, Post, ImageUpload
from mediumeditor.admin import MediumEditorAdmin
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(ImageUpload)
admin.site.register(Post)
