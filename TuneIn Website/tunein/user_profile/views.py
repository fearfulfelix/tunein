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
            'following': following}
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
            'following': following}
        template = loader.get_template('user_profile/index.html')
        return HttpResponse(template.render(con))
    else:
        #send user to login
        return  HttpResponseRedirect('/')


#processes a follow request, will also account for unfollowing soon
#users also cant follow themselves because thats dumb.
def follow_user(request):
    print(request.GET.get('target'))
    target = User.objects.get(username= request.GET.get('target'))
    follower = request.user
    if target.id != follower.id:

        if Following.objects.filter(user= target, follower = follower):
            print("user is already followed")
            data = {'message': 'user is already followed'}
        else:
            follow = Following.objects.create(user= target, follower = follower)
            data = {'message': 'user followed'}
        print("clicked")

    else:
        data = {'message': 'you cant follow yourself!'}
    #remove this maybe
    
    return JsonResponse(data)


    #processes a follow request, will also account for unfollowing soon
#users also cant follow themselves because thats dumb.
def friend_request_user(request):
    print(request.GET.get('target'))
    target = User.objects.get(username= request.GET.get('target'))
    potentialFriend = request.user
    if target.id != potentialFriend.id:

        if Friends.objects.filter(user= target, friend = potentialFriend):
            print("Already friends...")
            data = {'message': 'Already Friends!'}
        elif  FriendRequest.objects.filter(user= target, friend = potentialFriend):
            print("request already sent")
            data = {'message': 'A request has already been sent!'}
        else:
            friend = FriendRequest.objects.create(user= target, friend = potentialFriend)
            data = {'message': 'A request has been sent!'}
        print("clicked")

    else:
        data = {'message': 'you cannot add yourself as a friend!'}
    #remove this maybe
    
    return JsonResponse(data)

def send_notifcations(request):
    FRS = []
    data = {'requests':FRS}
    #check for active requests
    requests = FriendRequest.objects.filter(user= request.user)
    if requests:
        for r in requests:
            #modify the data?
            user = getattr(r, 'user')
            friend = getattr(r, 'friend')
            FR = {'target':getattr(user,'username'),
                    'sender': getattr(friend, 'username')}
            FRS.append(FR)
    #check for other notifications? 
    #maybe later...
    return JsonResponse(data)

def accept_friend_request(request):
    target = User.objects.get(username= request.GET.get('target'))
    potentialFriend = User.objects.get(username= request.GET.get('sender'))
    if target.id != potentialFriend.id:
        if Friends.objects.filter(user= target, friend = potentialFriend):
            print("Already friends...")
            data = {'message': 'Already Friends!'}
        else:
            friend = Friends.objects.create(user= target, friend = potentialFriend)
            frendRequest = FriendRequest.objects.filter(user= target, friend = potentialFriend)
            frendRequest.remove()
            data = {'message': 'A request has been sent!'}
        print("clicked")

    else:
        data = {'message': 'you cannot add yourself as a friend!'}

    #I dont think theres anything to return, but its just in case
    return JsonResponse(data)
