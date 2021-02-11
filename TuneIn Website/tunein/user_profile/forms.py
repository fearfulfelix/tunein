from django import forms


class loginForm(forms.Form):
    username = forms.CharField(label = 'username:')
    password = forms.CharField(label = 'Password:', widget = forms.PasswordInput)

