from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    User._meta.get_field('email')._unique = True
    ARTIST = 'ARTIST'
    FAN = 'FAN'
    account_type_choices = ((ARTIST,"ARTIST"),
                            (FAN, "FAN"))                  
    account_type = models.CharField(max_length= len(ARTIST), choices= account_type_choices, default=FAN)
    first_name = models.CharField(max_length=20,default="")
    last_name = models.CharField(max_length=20,default="")
    bio = models.CharField(max_length=500,default="n/a")
    photo = models.ImageField(upload_to='static/media/profilePictures')
    following = models.IntegerField(default = 0)
    followers = models.IntegerField(default = 0)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()