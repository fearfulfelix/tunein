from django.shortcuts import render
from django.http import HttpResponse


def loginIndex(request):
    return render(request, 'loginpage/index.html')

# Create your views here.
