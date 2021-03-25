from django.urls import path
from . import views

app_name = 'ajax'
urlpatterns = [
    path('', views.root, name='root'),
    path('follow_user', views.follow_user, name='follow_user'),
    path('friend_request_user', views.friend_request_user, name='friend_request_user'),
    path('send_notifcations', views.send_notifcations, name='send_notifcations'),
    path('accept_friend_request', views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request', views.reject_friend_request, name='reject_friend_request'),
    path('are_they_friends',views.are_they_friends,name='are_they_friends'),
    path('are_they_being_followed',views.are_they_being_followed,name='are_they_being_followed'),
    path('unfollow_user', views.unfollow_user, name='unfollow_user'),
    path('unfriend_user', views.unfriend_user, name='unfriend_user'),
    path('cancel_friend_request',views.cancel_friend_request,name='cancel_friend_request'),
    path('delete_notification',views.delete_notification,name='delete_notification'),
    path('likePost',views.likePost,name='likePost'),
    path('unlikePost',views.unlikePost,name='unlikePost'),
    path('isLiked',views.isLiked,name='isLiked'),
    path('getComments',views.getComments,name='getComments'),
    path('postComment',views.postComment,name='postComment')
]