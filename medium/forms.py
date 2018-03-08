from django import forms
from django.contrib.auth.models import User
from medium.models import UserProfile, Post, Comment
from crispy_forms.helper import FormHelper
from mediumeditor.widgets import MediumEditorTextarea
from froala_editor.widgets import FroalaEditor


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'password', 'confirm_password',
                  'email', 'first_name', 'last_name')

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "passwords do not match"
            )
    helper = FormHelper()


class UserEditForm(forms.ModelForm):

    class Meta():
        model = User
        fields = (
            'email', 'first_name', 'last_name')

    helper = FormHelper()


class UserProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        exclude = ('user',)
    helper = FormHelper()


class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('title', 'tags', 'content', 'featured_image')

        widgets = {
            'title': forms.Textarea(attrs={'class': 'post-title-input', 'placeholder': 'Title'}),
            'content': FroalaEditor(),
        }


class PostFeaturedImageForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('featured_image',)


class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('content',)

    helper = FormHelper()

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = "Write a response"
