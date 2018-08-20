# users/forms.py
from django import forms
from fil_auth.models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from registration.forms import RegistrationForm
from registration.users import UserModel
from registration.users import UsernameField

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        exclude = ()
class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        exclude = ()


## Model to set username = email
User = UserModel()

class MyRegForm(RegistrationForm):
    username = forms.CharField(max_length=254, required=False, widget=forms.HiddenInput())

    class Meta:
        fields = ("username", "email")
        model = User

    def clean_email(self):
        email = self.cleaned_data['email']
        self.cleaned_data['username'] = email
        return email
