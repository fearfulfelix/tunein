from django.shortcuts import render
from django.http import HttpResponse
from user_profile.forms import *
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from user_profile.models import User, Following, Friends
from news.forms import NewPostForm, NewCommentForm
from news.models import Post, Comment, Like,SharedPost
from datetime import datetime
from operator import itemgetter
import operator
from django.contrib.auth.models import Group
from PIL import Image
from django.core.files import File
from io import StringIO, BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
# Create your views here.

def home(request):
    return render(request, 'home.html')


#can we get rid of this?
def add(request):
    val1 = int(request.GET['num1'])
    val2 = int(request.GET['num2'])

    res = val1 + val2

    return render(request, 'results.html', {'result': res})


#the feed, essentially the users homepage.
def feed(request):
    sharedPosts = False
    if request.user.is_authenticated:
        following = Following.objects.filter(follower= request.user)
        following_list = []
        for f in following:
            following_list.append(getattr(f,'user'))
        if following:
            posts = Post.objects.filter(user_name__in=following_list)
            sharedPosts = SharedPost.objects.filter(user__in=following_list)
            sharedPosts = sharedPosts.order_by('-date_posted')
        else:
            posts = Post.objects.all()
        posts = posts.order_by('-date_posted')
        artist = request.user.groups.filter(name='artists').exists()

        friends_a = Friends.objects.filter(user= request.user)
        friends_b = Friends.objects.filter(friend= request.user)
        friends_list = []
        for f in friends_a:
            friends_list.append(getattr(f,'friend'))
        for f in friends_b:
            friends_list.append(getattr(f,'user'))
        friends_sharedPosts =SharedPost.objects.filter(user__in= friends_list)
        if friends_sharedPosts:
            print(friends_sharedPosts)
        
        if sharedPosts:
            print(sharedPosts)
            l_posts = list(posts)
            l_shared = list(sharedPosts)
            l_posts.extend(l_shared)
            print(l_posts)
            all_posts = sorted(l_posts,key=lambda x: x.get_date(),reverse=True)
            print(all_posts)
            test = {'posts': all_posts, 'artist': artist}
        else:
            test = {'posts': posts, 'artist': artist}
        
        if sharedPosts and friends_sharedPosts:
            l_f_sp = list(friends_sharedPosts)
            all_posts.extend(l_f_sp)
            print(all_posts)
            all_posts = list(set(sorted(all_posts,key=lambda x: x.get_date(),reverse=True)))
            print(all_posts)
            test = {'posts': all_posts, 'artist': artist}

        return render(request, 'news.html', test)
    else:
        return HttpResponseRedirect('/') 


#settings page, needs more settings
def settings(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.POST['formType'] == 'Update Bio':
                form = bioForm(request.POST)
                if(form.is_valid()):
                    newBio = form.cleaned_data['bio']
                    request.user.profile.bio = newBio
                    request.user.profile.save()
            else:
                form = nameForm(request.POST)
                if(form.is_valid()):
                    newFirst = form.cleaned_data['first_name']
                    newLast = form.cleaned_data['last_name']
                    if newFirst != "" and newLast != "":
                        request.user.profile.first_name = newFirst
                        request.user.profile.last_name = newLast
                        request.user.profile.save()
        else:
            name= nameForm()
            bio = bioForm()
            return render(request,'settings.html',{"nameForm":name, "bioForm":bio})
        return HttpResponseRedirect('feed')
    else:
        return HttpResponseRedirect('/')

#creates a profile to match the newly created user 
def createProfile(request):
    errmsg = ""
    if request.user.is_authenticated:
        if request.user.profile.first_name == "":
            if request.method== 'POST':
                p = profileForm(request.POST, request.FILES)
                if p.is_valid():
                    try:
                        cleanProfile = p.cleaned_data
                        first = cleanProfile['first_name']
                        last = cleanProfile['last_name']
                        bio = cleanProfile['bio']
                        img = Image.open(cleanProfile['profilePicture'])
                        Artist = cleanProfile['artist']

                        #image processing stuff goes here :)
                        img_width, img_height = img.size
                        c_img = img.crop(((img_width - min(img.size)) // 2, (img_height - min(img.size)) // 2, (img_width + min(img.size)) // 2, (img_height + min(img.size)) // 2))
                        c_img = c_img.resize((250,250))
                        thumb_io = BytesIO()
                        c_img.save(thumb_io, format='PNG')
                        thumb_file = File(thumb_io, name=cleanProfile['profilePicture'].name)
                        #image processing is done, model gets saved

                        request.user.profile.first_name = first
                        request.user.profile.last_name = last
                        request.user.profile.bio = bio
                        request.user.profile.photo = thumb_file
                        request.user.profile.save()
                        if Artist:
                            artist_group = Group.objects.get(name='artists') 
                            artist_group.user_set.add(request.user)
                        else:
                            fan_group = Group.objects.get(name='fans') 
                            fan_group.user_set.add(request.user)
                        return HttpResponseRedirect('feed')
                    except ValueError:
                        errmsg ="something went wrong, please try again."
                        profile = profileForm()
                        return render(request,'createProfile.html',{'profileForm':profile,'message':errmsg})    
            else:
                profile = profileForm()
                return render(request,'createProfile.html',{'profileForm':profile,'message':errmsg})
        else:
            return HttpResponseRedirect('feed')  
    else:
        return HttpResponseRedirect('login')

#logs the user out, and sends them to the login page
def processLogout(request):
    logout(request)
    return HttpResponseRedirect('/')


#the login page, now with error messages :D
def loginIndex(request):
    #blank message
    errmsg = ""
    if request.method =='POST':
        if request.POST['formType'] == 'Login':   
            form = loginForm(request.POST)
            if form.is_valid():
                credentials = form.cleaned_data
                user = authenticate(username=credentials['username'],
                                    password=credentials['password'])
                if user is not None:
                    login(request, user)
                    if user.profile.first_name == "":
                        return HttpResponseRedirect('createProfile')
                    else:
                        return HttpResponseRedirect('feed')
                else:
                    errmsg="User not found, please try again."
            else:
                errmsg="User not found, please try again."
        elif request.POST['formType'] == 'Create New Account':
            form = registrationForm(request.POST)
            if form.is_valid():
                credentials = form.cleaned_data
                username = credentials['username']
                email = credentials['email']
                created = User.objects.filter(email=email,username=username)
                created2 = User.objects.filter(email=email)
                created3 = User.objects.filter(username=username)

                if created:
                    errmsg="An account with that username or email already exists."
                elif created2:
                    errmsg="An account with that email already exists."
                elif created3:
                    errmsg="An account with that username already exists."
                else:
                    user = User.objects.create_user(username=credentials['username'],
                    email=credentials['email'],
                    password=credentials['password'])
                    login(request,user)
                    return HttpResponseRedirect('createProfile')
    form = loginForm()
    rform = registrationForm()
    return render(request, 'loginpage/index.html', {'LoginForm': form,'RegistrationForm': rform,"message":errmsg})


#allows users to create posts, if they're logged in and have the canpost permission(exclusive to the artist group)
def createPost(request):
    if request.user.is_authenticated and request.user.has_perm('canPost'):
        if request.method== 'POST':
            p = NewPostForm(request.POST, request.FILES)
            try:
                if p.is_valid:
                    obj = p.save(commit=False)
                    obj.user_name = request.user
                    obj.save()
                    return HttpResponseRedirect('feed')
            except ValueError:
                return render(request,'createPost.html',{'postForm':p,"message":"Error creating post, please double check your info and try again."})
        else:
            p = NewPostForm()
            return render(request,'createPost.html',{'postForm':p})
    else:
        return "You dont have permission to create posts."