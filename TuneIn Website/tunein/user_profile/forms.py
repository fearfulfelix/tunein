from django import forms

#forms used to login and register users
#do not replace any of these with a model form, it breaks EVERYTHING
#-Felix

class loginForm(forms.Form):
    username = forms.CharField(label = 'username:')
    password = forms.CharField(label = 'Password:', widget = forms.PasswordInput)

class registrationForm(forms.Form):
    username = forms.CharField(label = 'username:')
    email = forms.CharField(label="email", widget= forms.EmailInput)
    password = forms.CharField(label = 'Password:', widget = forms.PasswordInput)

class profileForm(forms.Form):
    first_name = forms.CharField(label = 'First Name:')
    last_name = forms.CharField(label = 'Last Name:')
    bio = forms.CharField(label = 'bio:', widget=forms.Textarea)

#these are individual forms for the settings page

class nameForm(forms.Form):
    first_name = forms.CharField(label = 'First Name:')
    last_name = forms.CharField(label = 'Last Name:')

class bioForm(forms.Form):
    bio = forms.CharField(label = 'bio:', widget=forms.Textarea)
    