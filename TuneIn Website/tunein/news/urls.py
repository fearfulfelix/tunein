from django.urls import path

from . import views

urlpatterns = [
    path('', views.loginIndex, name='login'),
    path('add', views.add, name='add'),
    path('home', views.home, name='home'),
    path('feed', views.feed, name="feed"),
    path('processing', views.processLogin, name='processLogin'),
    path('settings', views.settings, name="settings"),
    path('logOut',views.processLogout, name='logout'),
    path('register', views.processRegistration, name='register'),
    path('createPost', views.createPost, name='createPost'),
    path('createProfile',views.createProfile, name='createProfile'),
    path('processProfile',views.processProfile,name ='processProfile'),
    path('processSettings',views.processSettings, name='processSettings')
]
#path('processPost',views.processPost, name="processPost"),