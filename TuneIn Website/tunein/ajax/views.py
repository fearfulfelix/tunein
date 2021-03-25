from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from user_profile.models import User, Following,FriendRequest, Friends, Notification, NotificationBridge
from news.models import Post,Like,Comment
# Create your views here.

#processes a follow request, will also account for unfollowing soon
#users also cant follow themselves because thats dumb.
def root(request):
    return null
def follow_user(request):
    target = User.objects.get(username= request.GET.get('target'))
    follower = request.user
    if target.id != follower.id:

        if Following.objects.filter(user= target, follower = follower):
            data = {'message': 'user is already followed'}
        else:
            follow = Following.objects.create(user= target, follower = follower)
            bridge = NotificationBridge.objects.create(notificationType='Follow', following=follow)
            newNotif = Notification.objects.create(source=bridge, receiver=target)
            data = {'message': 'user followed'}
    else:
        data = {'message': 'you cant follow yourself!'}
    #remove this maybe
    
    return JsonResponse(data)


    #processes a follow request, will also account for unfollowing soon
#users also cant follow themselves because thats dumb.
def friend_request_user(request):
    target = User.objects.get(username= request.GET.get('target'))
    potentialFriend = request.user
    if target.id != potentialFriend.id:

        if Friends.objects.filter(user= target, friend = potentialFriend):
            data = {'message': 'Already Friends!'}
        elif  FriendRequest.objects.filter(user= target, friend = potentialFriend):
            data = {'message': 'A request has already been sent!'}
        else:
            friend = FriendRequest.objects.create(user= target, friend = potentialFriend)
            data = {'message': 'A request has been sent!'}
            bridge = NotificationBridge.objects.create(notificationType='FriendRequest', friendRequest=friend)
            newNotif = Notification.objects.create(source=bridge, receiver=target)

    else:
        data = {'message': 'you cannot add yourself as a friend!'}
    #remove this maybe
    
    return JsonResponse(data)

def send_notifcations(request):
    results = []
    data = {'notifications':results}
    #check for active notifications
    notifs = Notification.objects.filter(receiver= request.user)
    if notifs:
        for n in notifs:
            #get funky with it
            src = getattr(n,'source')
            if getattr(src,'notificationType') == 'Follow':
                fromWho = getattr(getattr(getattr(src,'following'),'follower'),'username')
                notifInfo = {'type': getattr(src,'notificationType'),'from': fromWho}
                results.append(notifInfo)
            if getattr(src,'notificationType') == 'Friend':
                fromWho = getattr(getattr(getattr(src,'friend'),'user'),'username')
                notifInfo = {'type': getattr(src,'notificationType'),'from': fromWho}
                results.append(notifInfo)
            if getattr(src,'notificationType') == 'FriendRequest':
                fromWho = getattr(getattr(getattr(src,'friendRequest'),'friend'),'username')
                notifInfo = {'type': getattr(src,'notificationType'),'from': fromWho}
                results.append(notifInfo)
    return JsonResponse(data)

def accept_friend_request(request):
    target = User.objects.get(username= request.user.username)
    potentialFriend = User.objects.get(username= request.GET.get('target'))
    if target.id != potentialFriend.id:
        if Friends.objects.filter(user= target, friend = potentialFriend):
            data = {'message': 'Already Friends!'}
        else:
            friend = Friends.objects.create(user= target, friend = potentialFriend)
            FriendRequest.objects.filter(user= target, friend = potentialFriend).delete()
            bridge = NotificationBridge.objects.create(notificationType='Friend', friend=friend)
            newNotif = Notification.objects.create(source=bridge, receiver=potentialFriend)
            data = {'message': 'Accepted!'}

    else:
        data = {'message': 'you cannot add yourself as a friend!'}

    #I dont think theres anything to return, but its just in case
    return JsonResponse(data)

def are_they_friends(request):
    data = {}
    target = User.objects.get(username= request.user.username)
    potentialFriend = User.objects.get(username= request.GET.get('target'))
    if target.id != potentialFriend.id:
        if Friends.objects.filter(user= target, friend = potentialFriend):
            data = {'Friends': 'True'}
        elif Friends.objects.filter(user= potentialFriend, friend = target):
            data = {'Friends': 'True'}
        elif FriendRequest.objects.filter(user= potentialFriend, friend =  target):
            data = {'Friends': 'Requested'}
        else:
            data = {'Friends':'False'}
        
    return JsonResponse(data)

def are_they_being_followed(request):
    data = {}
    target =User.objects.get(username= request.GET.get('target')) 
    potentialFriend = User.objects.get(username= request.user.username)
    if target.id != potentialFriend.id:
        if Following.objects.filter(user= target, follower = potentialFriend):
            data = {'followBool': True}
        else:
            data = {'followBool':False}
        
    return JsonResponse(data)

def unfollow_user(request):
    data = {}
    follower = User.objects.get(username= request.user.username)
    target = User.objects.get(username= request.GET.get('target'))
    if target.id != follower.id:
        if Following.objects.filter(user= target, follower = follower):
            Following.objects.filter(user= target, follower = follower).delete()

        
        return JsonResponse(data)
def unfriend_user(request):
    data = {}
    target = User.objects.get(username= request.user.username)
    potentialFriend = User.objects.get(username= request.GET.get('target'))
    if target.id != potentialFriend.id:
        if Friends.objects.filter(user= target, friend = potentialFriend):
            Friends.objects.filter(user= target, friend = potentialFriend).delete()
        elif Friends.objects.filter(user=potentialFriend , friend = target):
            Friends.objects.filter(user=potentialFriend , friend = target).delete()
        return JsonResponse(data)
def cancel_friend_request(request):
    data = {}
    potentialFriend = User.objects.get(username= request.user.username)
    
    target = User.objects.get(username= request.GET.get('target'))
    if target.id != potentialFriend.id:
        if Friends.objects.filter(user= target, friend = potentialFriend) or Friends.objects.filter(user= potentialFriend, friend =  target):
            data = {'message': 'Already Friends!'}
        else:
            FriendRequest.objects.filter(user=target , friend =potentialFriend ).delete()
            data = {'message': 'Request cancelled'} 
    else:
        data = {'message': 'Error same user!'}    
    return JsonResponse(data)

def reject_friend_request(request):
    target = User.objects.get(username= request.user.username)
    potentialFriend = User.objects.get(username= request.GET.get('target'))
    if target.id != potentialFriend.id:
        if Friends.objects.filter(user= target, friend = potentialFriend):
            data = {'message': 'Already Friends!'}
        else:
            data = {'message': 'Denied!'}
        FriendRequest.objects.filter(user= target, friend = potentialFriend).delete()
    else:
        data = {'message': 'you cannot add yourself as a friend!'}

    #I dont think theres anything to return, but its just in case
    return JsonResponse(data)

def delete_notification(request):
    data ={'message':'dismissed'}
    if request.GET.get('type') == 'Follow':
        potentialFriend = User.objects.get(username= request.GET.get('from'))
        follow =  Following.objects.get(user=request.user, follower= potentialFriend)
        NotificationBridge.objects.get(notificationType = request.GET.get('type'), following= follow).delete()
    elif request.GET.get('type') == 'Friend':
        potentialFriend = User.objects.get(username= request.GET.get('from'))
        friend =  Friends.objects.get(user=potentialFriend, friend= request.user) 
        NotificationBridge.objects.get(notificationType = request.GET.get('type'), friend= friend).delete()
    elif request.GET.get('type') == 'FriendRequest':
        friendRequest =  FriendRequest.objects.get(user=request.user, friend= request.GET.get('from'))
        NotificationBridge.objects.get(notificationType = request.GET.get('type'), friendRequest= friend).delete()
    return JsonResponse(data)


def likePost(request):
    data={}
    post = Post.objects.get(id=request.GET.get('postID'))
    if post:
        alreadyLiked = Like.objects.filter(originPost=post, user = request.user)
        if alreadyLiked:
            data={'message':'already Liked'}
        else:
            like = Like.objects.create(originPost=post, user = request.user)
            data={'message':'post liked'}
    return JsonResponse(data)

def unlikePost(request):
    data={}
    post = Post.objects.get(id=request.GET.get('postID'))
    if post:
        alreadyLiked = Like.objects.filter(originPost=post, user = request.user)
        if alreadyLiked:
            alreadyLiked.delete()
            data={'message':'Unliked'}
        else:
            data={'message':'post was never liked'}
    return JsonResponse(data)
    
def isLiked(request):
    data={}
    post = Post.objects.get(id=request.GET.get('postID'))
    if post:
        alreadyLiked = Like.objects.filter(originPost=post, user = request.user)
        if alreadyLiked:
            alreadyLiked.delete()
            data={'liked':True}
        else:
            data={'liked':False}
    return JsonResponse(data)