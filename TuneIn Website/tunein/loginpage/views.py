from django.shortcuts import render
from django.http import HttpResponse
from user_profile.forms import loginForm
from django.http import HttpResponseRedirect
from django.template import loader


def loginIndex(request):
    form = loginForm()
    con = {'LoginForm' :form}
    print(con['LoginForm'])
    print("UNF")

    return render(request, 'loginpage/index.html',con)
