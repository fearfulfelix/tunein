from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import User
from news.models import Post
# Create your views here.

#profile page
def index(request):
    #makes sure user is logged in
    if request.user.is_authenticated:
        posts = {}
        #attempting to pull user, role, and posts from GET
        try:
            sample_user = User.objects.get(username= request.GET.get('username'))
            artist = sample_user.groups.filter(name='artists').exists()
            if artist:
                posts = Post.objects.filter(user_name__username =request.GET.get('username'))
                for post in posts:
                    print(post)
            con = {'user': sample_user,
            'artist': artist,
            'posts':posts}
        #if the user in GET can't be found, show the logged in user instead
        except User.DoesNotExist:
            print("USER NOT FOUND, SHOWING LOGGED IN PROFILE")
            sample_user = request.user
            artist = sample_user.groups.filter(name='artists').exists()
            if artist:
                posts = Post.objects.filter(user_name__username =request.user.username)
                posts = posts.order_by('-date_posted')
                for post in posts:
                    print(post)
            con = {'user': sample_user,
            'artist': artist,
            'posts':posts}
        template = loader.get_template('user_profile/index.html')
        return HttpResponse(template.render(con))
    else:
        #send user to login
        return  HttpResponseRedirect('/')


