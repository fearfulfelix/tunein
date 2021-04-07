from django import forms
from .models import Comments, Post


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'pic', 'choose_file' ,'tags']
        widgets={'description':forms.Textarea(attrs={'cols':50})}


class NewCommentForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ['comment']