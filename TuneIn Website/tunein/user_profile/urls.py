from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='user_profile'),
    path('follow_user', views.follow_user, name='follow_user')
]