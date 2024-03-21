from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout,get_user
from django.contrib import messages
from .models import Contact
from datetime import datetime
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    return render(request, 'index.html')

def faqs(request):
    return render(request, "faqs.html")



def contact(request):
    if(request.method=="POST"):
        name=request.POST['name']
        email=request.POST['email']
        subject=request.POST['subject']
        message=request.POST['message']

        contact=Contact(name=name, email=email, subject=subject, message=message, date=datetime.today())
        contact.save()
        messages.success(request, "Message sent Successfully")
        return HttpResponseRedirect(request.path_info)
    return render(request, 'contact.html')