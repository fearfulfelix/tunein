from django.urls import path

from . import views

urlpatterns = [
    path('', views.loginIndex, name='login'),
    path('add', views.add, name='add'),
    path('home', views.home, name='home'),
    path('feed', views.feed, name="feed"),
    path('processing', views.processLogin, name='ignoreMe'),
    path('logOut',views.processLogout, name='logout')
]
