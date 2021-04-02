from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from news.models import Comment,SharedPost


# Create your models here.
#profile is basically an extension of the user model provided by django
#it has all the extra fields that arent in user
#it also modifies the user model to ensure email addresses are unique to avoid complications
class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    User._meta.get_field('email')._unique = True
    first_name = models.CharField(max_length=20,default="")
    last_name = models.CharField(max_length=20,default="")
    bio = models.CharField(max_length=500,default="n/a")
    photo = models.ImageField(upload_to='static/media/profilePictures')

    def __str__(self):
        return self.user.username

#creates and modifies the profile when the user is modified
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

#a model containing a user and a follower, this is used to store the users following and being followed
#only artists should be allowed to be followed
class Following(models.Model):
    #id is the primary key in this model, and is created by django itself
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='target')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

#a model containing a user and a friend, this is used to store the relationship between friends <3
#at the moment, two entries are required to be friends, but this is redundant and we should fix it if possible
class Friends(models.Model):
    #id is the primary key in this model, and is created by django itself
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='targetFriend')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sourceFriend')

#a model containing a user and a friend, this is used to store the users friend requests 
class FriendRequest(models.Model):
    #id is the primary key in this model, and is created by django itself
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendRequestTarget')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='RequestSender')

#this is a wip, not exactly sure where to go with it, sorry
class Music(models.Model):
    name = models.CharField(default="", max_length =32)
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
    release_date = models.DateTimeField(default =datetime.now())
    album_art = models.ImageField(upload_to='static/media/albumPictures')
    genre = models.CharField(default="", max_length = 20)
    explicit = models.BooleanField(default=False)
    partOfAlbum =models.BooleanField(default=False)
    albumID = models.CharField(default="",max_length = 40)

    def __str__(self):
        return self.name

class NotificationBridge(models.Model):
    notificationType = models.CharField(max_length=20,default="NONE")
    friendRequest = models.OneToOneField(FriendRequest, on_delete=models.CASCADE, null=True)
    following = models.OneToOneField(Following, on_delete=models.CASCADE, null=True)
    friend = models.OneToOneField(Friends, on_delete=models.CASCADE, null=True)
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, null=True)
    share = models.OneToOneField(SharedPost, on_delete=models.CASCADE, null=True)
    #add more for each other notification type

class Notification(models.Model):
    source = models.OneToOneField(NotificationBridge, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifReceiver')

