from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .validators import validate_file_extension
import os


# Create your models here.
class Post(models.Model):
    description = models.CharField(max_length=255, blank=True)
    pic = models.ImageField(upload_to='static/media/postPictures', blank=True, null=True)
    choose_file = models.FileField(upload_to='static/media/mediaFiles', validators=[validate_file_extension], blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def get_date(self):
        return self.date_posted
    
    def extension(self):
        video = ['.mp4', '.mov', '.m4v', '.avi']
        audio = ['.wav', '.mp3', '.flac', '.mkv', '.aac'] 
        name, extension = os.path.splitext(self.choose_file.name)
        if extension in video: return "video"
        elif extension in audio: return "audio"
        return None

class SharedPost(models.Model):
    originPost = models.ForeignKey(Post, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=255, blank=True)

    def get_date(self):
        return self.date_posted


class Comment(models.Model):
    originPost = models.ForeignKey(Post, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000) 

class Like(models.Model):
    originPost = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
