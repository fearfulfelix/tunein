from django import forms

#forms used to login and register users
#do not replace any of these with a model form, it breaks EVERYTHING
#-Felix

class loginForm(forms.Form):
    username = forms.CharField(label = 'Username:')
    password = forms.CharField(label = 'Password:', widget = forms.PasswordInput)

class registrationForm(forms.Form):
    username = forms.CharField(label = 'Username:')
    email = forms.CharField(label="Email", widget= forms.EmailInput)
    password = forms.CharField(label = 'Password:', widget = forms.PasswordInput)

class profileForm(forms.Form):
    first_name = forms.CharField(label = 'First Name:')
    last_name = forms.CharField(label = 'Last Name:')
    profilePicture = forms.ImageField(label = 'Profile picture')
    bio = forms.CharField(label = 'Bio:', widget=forms.Textarea)
    artist = forms.BooleanField(label = 'Artist:')

#these are individual forms for the settings page

class nameForm(forms.Form):
    first_name = forms.CharField(label = 'First Name:')
    last_name = forms.CharField(label = 'Last Name:')

class bioForm(forms.Form):
    bio = forms.CharField(label = 'Bio:', widget=forms.Textarea)
    