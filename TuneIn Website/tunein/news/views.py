from django.shortcuts import render
from django.http import HttpResponse
from user_profile.forms import loginForm, registrationForm, profileForm
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from user_profile.models import User
from news.forms import NewPostForm, NewCommentForm
from news.models import Post, Comments, Like
# Create your views here.
#I went through and added comments, feel free to modify them 
#-Felix

#?
def home(request):
    return render(request, 'home.html')

#can we get rid of this?
def add(request):
    val1 = int(request.GET['num1'])
    val2 = int(request.GET['num2'])

    res = val1 + val2

    return render(request, 'results.html', {'result': res})

#the feed, essentially te users homepage.
def feed(request):
    if request.user.is_authenticated:
        return render(request, 'news.html')
    else:
        return HttpResponseRedirect('/') 

#settings page, needs to be functional
def settings(request):
    if request.user.is_authenticated:
        return render(request,'settings.html')
    else:
        return HttpResponseRedirect('/')
    

#processes the login form from the login page.
#   uses the built in django authentication system to validate the provided user information
#   needs to provide error information to users upon failed login
#   sends user to the feed, UNLESS they haven't created a profile, in that case they go to createProfile
def processLogin(request):
    if request.method == 'POST':
        print("post")
        form = loginForm(request.POST)
        print(form)

        if form.is_valid:
            print("valid")
            credentials = form.cleaned_data
            user = authenticate(username=credentials['username'],
                                password=credentials['password'])
            if user is not None:
                print("not none")
                login(request, user)
                if user.profile.first_name == "":
                    return HttpResponseRedirect('createProfile')
                else:
                    return HttpResponseRedirect('feed')
            else:
                print("user does not exist")
                return HttpResponseRedirect('/')
        else:
            print("form error")
            return HttpResponseRedirect('/')

#processes the user registration form from the login page
#   simmilar to processlogin, where it uses the built in authentication system to validate users
#   needs to provide error information to users upon failed registration
#   this now sends users to the profile creation page
def processRegistration(request):
    if request.method == 'POST':
        print("post")
        form = registrationForm(request.POST)
        print(form)
        if form.is_valid:
            print("valid")
            credentials = form.cleaned_data
            username = credentials['username']
            email = credentials['email']
            created = User.objects.filter(email=email,username=username)
            print(created)
            if created:
                print("user already exists")
                return HttpResponseRedirect('/')
            else:
                user = User.objects.create_user(username=credentials['username'],
                email=credentials['email'],
                password=credentials['password'])
                print(user)
                login(request,user)
                print("send user to profile creation page")
                return HttpResponseRedirect('createProfile')
    return None            

#creates a profile to match the newly created user 
def createProfile(request):
    if request.user.is_authenticated and request.user.profile.first_name == "":
        profile = profileForm()
        return render(request,'createProfile.html',{'profileForm':profile})
    else:
        return HttpResponseRedirect('processProfile')

#processes the form retrieved from createProfile
#   Updates the user.profile model currently logged in    
def processProfile(request):
    if request.user.is_authenticated and request.user.profile.first_name == "":
        if request.method== 'POST':
            p = profileForm(request.POST)
            if p.is_valid():
                cleanProfile = p.cleaned_data
                first = cleanProfile['first_name']
                last = cleanProfile['last_name']
                bio = cleanProfile['bio']
                request.user.profile.first_name = first
                request.user.profile.last_name = last
                request.user.profile.bio = bio
                request.user.profile.save()
    return HttpResponseRedirect('feed')

#logs the user out, and sends them to the login page
def processLogout(request):
    print("logging user out")
    logout(request)
    print("user logged out")
    return HttpResponseRedirect('/')

#the login page, the two forms send the user to processLogin and processRegistration
def loginIndex(request):
    form = loginForm()
    rform = registrationForm()
    return render(request, 'loginpage/index.html', {'LoginForm': form,'RegistrationForm': rform})

#allows users to create posts, if they're logged in and have the canpost permission(exclusive to artists)
#P sends users to processPost upon submitting
def createPost(request):
    print("entered")
    if request.user.is_authenticated and request.user.has_perm('canPost'):
        p = NewPostForm()
        return render(request,'createPost.html',{'postForm':p, 'user':request.user})
    else:
        return "You dont have permission to create posts."

#processes posts recieved from createPost
#authenticates the user and their permissions again(just in case)
#then validates the form, and creates a post model to store in the database
#sends users back to the feed once complete.
def processPost(request):
    if request.user.is_authenticated and request.user.has_perm('canPost'):
        if request.method== 'POST':
            p = NewPostForm(request.POST)
            print(p)
            if p.is_valid:
                print("valid")
                CleanPost = p.cleaned_data
                desc = CleanPost['description']
                pic = CleanPost['pic']
                tags = CleanPost['tags']
                print(desc)
                result = Post.objects.create(description=desc,pic=pic, tags=tags, user_name=request.user)
                print("created!")

    return HttpResponseRedirect('feed')