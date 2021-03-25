from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.template import loader
from .models import User, Following,FriendRequest, Friends
from news.models import Post
# Create your views here.

#profile page
def index(request):
    #makes sure user is logged in
    if request.user.is_authenticated:
        followers = 0
        friends = 0
        posts = {}
        #attempting to pull user, role, and posts from GET
        try:
            sample_user = User.objects.get(username= request.GET.get('username'))
            artist = sample_user.groups.filter(name='artists').exists()
            if artist:
                followers = Following.objects.filter(user= sample_user).count()
                posts = Post.objects.filter(user_name__username =request.GET.get('username'))
                posts = posts.order_by('-date_posted')
                for post in posts:
                    print(post)
            following = Following.objects.filter(follower= sample_user).count()
            con = {'user': sample_user,
            'artist': artist,
            'posts':posts,
            'followers': followers,
            'following': following,
            'otherUser':True}
        #if the user in GET can't be found, show the logged in user instead
        except User.DoesNotExist:
            print("USER NOT FOUND, SHOWING LOGGED IN PROFILE")
            sample_user = request.user
            followers = 0
            friends = 0
            artist = sample_user.groups.filter(name='artists').exists()
            if artist:
                followers = Following.objects.filter(user= request.user).count()
                posts = Post.objects.filter(user_name__username =request.user.username)
                posts = posts.order_by('-date_posted')
                for post in posts:
                    print(post)
            following = Following.objects.filter(follower= request.user).count()
            con = {'user': sample_user,
            'artist': artist,
            'posts':posts,
            'followers': followers,
            'following': following,
            'otherUser':False}
        template = loader.get_template('user_profile/index.html')
        return HttpResponse(template.render(con))
    else:
        #send user to login
        return  HttpResponseRedirect('/')

