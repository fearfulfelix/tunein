from django import forms


class loginForm(forms.Form):
    username = forms.CharField(label = 'username:')
    password = forms.CharField(label = 'Password:', widget = forms.PasswordInput)

class registrationForm(forms.Form):
    username = forms.CharField(label = 'username:')
    email = forms.CharField(label="email", widget= forms.EmailInput)
    password = forms.CharField(label = 'Password:', widget = forms.PasswordInput)