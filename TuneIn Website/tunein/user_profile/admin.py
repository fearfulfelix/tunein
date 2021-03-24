from django.contrib import admin
from .models import Profile, Music, Following, Friends, FriendRequest,Notification,NotificationBridge
# Register your models here.
admin.site.register(Profile)
admin.site.register(Music)
#unregister me plz
admin.site.register(Following)
admin.site.register(Friends)
admin.site.register(FriendRequest)
admin.site.register(Notification)
admin.site.register(NotificationBridge)
