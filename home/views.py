from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout,get_user
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')



def support(request):
    #  messages.success(request, "Welcome to Support")
     return render(request, 'support.html')