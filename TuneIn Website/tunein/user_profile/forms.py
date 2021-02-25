from django import forms

#forms used to login and register users
#do not replace with a model form, it breaks EVERYTHING
#-Felix

class loginForm(forms.Form):
    username = forms.CharField(label = 'username:')
    password = forms.CharField(label = 'Password:', widget = forms.PasswordInput)

class registrationForm(forms.Form):
    username = forms.CharField(label = 'username:')
    email = forms.CharField(label="email", widget= forms.EmailInput)
    password = forms.CharField(label = 'Password:', widget = forms.PasswordInput)