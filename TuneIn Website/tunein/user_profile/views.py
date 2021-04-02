from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.template import loader
from .models import User, Following,FriendRequest, Friends
from news.models import Post, SharedPost
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
            sharedPosts = SharedPost.objects.filter(user=sample_user)
            if sharedPosts:
                sharedPosts = sharedPosts.order_by('-date_posted')
                l_posts = list(posts)
                l_shared = list(sharedPosts)
                l_posts.extend(l_shared)
                print(l_posts)
                all_posts = sorted(l_posts,key=lambda x: x.get_date(),reverse=True)
                print(all_posts)
                posts = all_posts
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
            sharedPosts = SharedPost.objects.filter(user=sample_user)
            if sharedPosts:
                sharedPosts = sharedPosts.order_by('-date_posted')
                l_posts = list(posts)
                l_shared = list(sharedPosts)
                l_posts.extend(l_shared)
                print(l_posts)
                all_posts = sorted(l_posts,key=lambda x: x.get_date(),reverse=True)
                print(all_posts)
                posts = all_posts
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

