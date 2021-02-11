from django.shortcuts import render
from django.http import HttpResponse
from user_profile.forms import loginForm
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
# Create your views here.


def home(request):
    return render(request, 'home.html')


def add(request):

    val1 = int(request.GET['num1'])
    val2 = int(request.GET['num2'])

    res = val1 + val2

    return render(request, 'results.html', {'result': res})


def feed(request):
    
    return render(request, 'news.html')

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
                login(request,user)
                return HttpResponseRedirect('feed')
            else:
                print("user does not exist")
                return HttpResponseRedirect('/') 
        else:
            print("form error")
            return HttpResponseRedirect('/') 

def processLogout(request):
    print("logging user out")
    logout(request)
    print("user logged out")
    return HttpResponseRedirect('/')

def loginIndex(request):
    form = loginForm()
    return render(request, 'loginpage/index.html',{'LoginForm' :form})
