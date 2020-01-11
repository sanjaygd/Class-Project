from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import ProfileImage,Profile

User = get_user_model()

class SignUpForm(UserCreationForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    


    class Meta:
        model = User
        fields = ['username','email', 'birth_date', 'password1', 'password2']


class ProfileImageForm(forms.ModelForm):
    

    class Meta:
        model = ProfileImage
        fields = ['image']


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['birth_date']