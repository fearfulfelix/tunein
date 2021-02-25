from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import User
# Create your views here.

def index(request):

    con = {}
    try:
        sample_user = User.objects.get(username= request.GET.get('username'))
        artist = sample_user.groups.filter(name='artists').exists()
        con = {'user': sample_user,
        'artist': artist}
        
    except User.DoesNotExist:
        print("UNF")

    template = loader.get_template('user_profile/index.html')
    return HttpResponse(template.render(con))


