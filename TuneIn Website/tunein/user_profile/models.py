from django.db import models


# Create your models here.
class user(models.Model):
    username = models.CharField(max_length=20, primary_key=True)

    ARTIST = 'ARTIST'
    FAN = 'FAN'
    account_type_choices = ((ARTIST,"ARTIST"),
                            (FAN, "FAN"))
    account_type = models.CharField(max_length= len(ARTIST), choices= account_type_choices, default=FAN)
    first_name = models.CharField(max_length=20,default="")
    last_name = models.CharField(max_length=20,default="")
    bio = models.CharField(max_length=500,default="")
    photo = models.ImageField(upload_to='static/media/profilePictures')
    following = models.IntegerField(default = 0)
    followers = models.IntegerField(default = 0)


    objects = models.Manager()
    def __str__(self):
        return self.username
