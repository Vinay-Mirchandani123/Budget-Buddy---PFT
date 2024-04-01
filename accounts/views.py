from django.shortcuts import render,redirect,HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout,get_user
from django.contrib import messages
from .models import Editprofile,User
from base.emails import account_activation_email
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    if request.user.is_authenticated:
       return render(request, 'index.html')
    return render(request, 'login.html')

def loginUser(request):
    
    if(request.method=="POST"):
        email=request.POST['email']
        password=request.POST['password']

        user = User.objects.filter(username = email)
        
        if not user.exists():
            messages.warning(request, "Account not Found")
            return HttpResponseRedirect(request.path_info)
        
        # if not user[0].profile.email_verified:
        #     messages.warning(request, "Email not verified")
        #     return HttpResponseRedirect(request.path_info)

        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            return redirect("/goal/dashboard")
        
        messages.success(request, "Invalid Credentials")
        return HttpResponseRedirect(request.path_info)
    
    return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    # messages.success(request, "Your Account has been Sucessfully Logged out")
    return redirect("login")

def register(request):
    if(request.method=="POST"):
        firstName=request.POST['firstName']
        lastName=request.POST['lastName']
        email=request.POST['email']
        phonenumber=request.POST['phonenumber']
        password=request.POST['password']
        conpassword=request.POST['conpassword']

        #check pass and conpass are same
        if(password!=conpassword):
            messages.warning(request, "Confirm Password should be same as Original Password")
            return HttpResponseRedirect(request.path_info)


        user = User.objects.filter(username = email)
        
        if user.exists():
            messages.warning(request, "Email already exist")
            return HttpResponseRedirect(request.path_info)
        user = User.objects.create_user(username=email, email=email, password=password, phone_number=phonenumber)
        user.first_name= firstName
        user.last_name = lastName
        user.save()
        messages.success(request, "Your Account has been Successfully Created")
        return HttpResponseRedirect(request.path_info)

        # # Trigger email verification
        # try:
        #     account_activation_email(email, user.profile.email_token)
        #     messages.success(request, "Your Account has been Successfully Created. Check your email for verification.")
        #     return HttpResponseRedirect(request.path_info)
        # except Exception as e:
        #     print("Error sending activation email:", str(e))
        #     messages.error(request, "Failed to send activation email.")
        #     return HttpResponseRedirect(request.path_info)
        
    return render(request, 'register.html')

def activate_email(request , email_token):
    try:
        user = Profile.objects.get(email_token= email_token)
        user.email_verified = True
        user.save()
        messages.success(request, "Email verified Successfully")
        return redirect('/accounts/login')
    except Exception as e:
        return HttpResponse('Invalid Email token')

@login_required
def editprofile(request):
    if request.method == "POST":
        # Get the current user
        user = request.user
        # Get the user's profile or create a new one if it doesn't exist
        profile, created = Editprofile.objects.get_or_create(user=user)
        
        # Update the profile fields
        if 'profileimage' in request.FILES:
            profile.profileimage = request.FILES['profileimage']
        # profile.profileimage = request.POST['profileimage']
        profile.namefirst = request.POST['namefirst']
        profile.lastname = request.POST['lastname']
        profile.about = request.POST['about']
        profile.job = request.POST['job']
        profile.country = request.POST['country']
        profile.address = request.POST['address']
        profile.phone = request.POST['phone']
        profile.email = request.POST['email']
        profile.twitter = request.POST['twitter']
        profile.facebook = request.POST['facebook']
        profile.instagram = request.POST['instagram']
        profile.linkedin = request.POST['linkedin']
        
        # Save the profile
        profile.save()
        
        messages.success(request, "Saved Changes Successfully")
        return HttpResponseRedirect(request.path_info)
    
    return render(request, "userprofile.html")
