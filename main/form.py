from django import forms

from main.models import Review,Profile

from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

from django.contrib.auth.models import User

class ReviewForm(forms.ModelForm):

    class Meta:

        model = Review

        fields = ['rating','comment']

class RegisterForm(UserCreationForm):

    class Meta:

        model = User

        fields = ['username','email','password1','password2']

class LoginForm(AuthenticationForm):

    class Meta:

        model = User

        feilds = ['username','password1','password2']


class UserUpdateForm(forms.ModelForm):

    class Meta:

        model = User

        fields = ['first_name','last_name','email']


class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:

        model = Profile
        
        fields = ['bio', 'location', 'profile_picture']  
