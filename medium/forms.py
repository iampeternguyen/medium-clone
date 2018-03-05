from django import forms
from django.contrib.auth.models import User
from medium.models import UserProfile
from crispy_forms.helper import FormHelper


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


class UserProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        exclude = ('user',)
    helper = FormHelper()
