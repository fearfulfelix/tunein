from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add', views.add, name='add'),
    path('home', views.home, name='home'),
    path('feed', views.feed, name="feed")
]
