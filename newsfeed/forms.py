from django import forms

class RegisterForm(forms.Form):
    name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget = forms.PasswordInput(), max_length=60)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=60)

class StatusForm(forms.Form):
    title = forms.CharField(max_length=60)
    content = forms.CharField(max_length=250)

class MessageForm(forms.Form):
    message = forms.CharField(max_length=250)