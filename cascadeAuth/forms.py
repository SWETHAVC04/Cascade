from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput
from captcha.fields import CaptchaField

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

class CaptchaForm(forms.Form):
    captcha = CaptchaField()

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['email']

class ResetPasswordForm(forms.Form):    
    password1 = forms.CharField(widget=PasswordInput())
    password2 = forms.CharField(widget=PasswordInput())
    class Meta:
        model = User
        fields = ['password1', 'password2']

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6, required=True)
    class Meta:
        model = User
        fields = ['otp']