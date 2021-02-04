from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import *
# Create your views here.

def index(request):
    #delete this chunk before sharing
    #sample_user = user(username = "burnt_parmesan", first_name = "Felix", last_name = "Turgeon")
    #sample_user.save()
    #end

    con = {}
    try:
        sample_user = user.objects.get(username= request.GET.get('username'))
        con = {'user': sample_user}
    except user.DoesNotExist:
        print("UNF")

    template = loader.get_template('user_profile/index.html')
    return HttpResponse(template.render(con))
