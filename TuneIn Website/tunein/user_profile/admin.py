from django.contrib import admin
from .models import Profile, Music, Following
# Register your models here.
admin.site.register(Profile)
admin.site.register(Music)
#unregister me plz
admin.site.register(Following)