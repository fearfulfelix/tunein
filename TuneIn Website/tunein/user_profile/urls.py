from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='user_profile'),
    path('follow_user', views.follow_user, name='follow_user'),
    path('friend_request_user', views.friend_request_user, name='friend_request_user'),
    path('send_notifcations', views.send_notifcations, name='send_notifcations')
]