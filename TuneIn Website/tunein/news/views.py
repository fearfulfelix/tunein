from django.shortcuts import render
from django.http import HttpResponse
from user_profile.forms import loginForm, registrationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from user_profile.models import User
# Create your views here.


def home(request):
    return render(request, 'home.html')


def add(request):
    val1 = int(request.GET['num1'])
    val2 = int(request.GET['num2'])

    res = val1 + val2

    return render(request, 'results.html', {'result': res})


def feed(request):
    if request.user.is_authenticated:# checks if user is logged in, redirects to login if false
        return render(request, 'news.html')
    else:
        return HttpResponseRedirect('/') 

def settings(request):
    return render(request, 'settings.html')


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
                return HttpResponseRedirect('feed')
            else:
                print("user does not exist")
                return HttpResponseRedirect('/')
        else:
            print("form error")
            return HttpResponseRedirect('/')

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
                return HttpResponseRedirect('feed')
    return None            

def processLogout(request):
    print("logging user out")
    logout(request)
    print("user logged out")
    return HttpResponseRedirect('/')


def loginIndex(request):
    form = loginForm()
    rform = registrationForm()
    return render(request, 'loginpage/index.html', {'LoginForm': form,'RegistrationForm': rform})
