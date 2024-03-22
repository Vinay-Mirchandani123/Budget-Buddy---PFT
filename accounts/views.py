from django.shortcuts import render,redirect,HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout,get_user
from django.contrib import messages
from .models import Profile,Editprofile
from base.emails import account_activation_email

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
        user = User.objects.create_user(username=email, email=email, password=password)
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

def editprofile(request):
    
    
#     profileimage= request.POST['profileimage']
     about= request.POST['about']
#     country= request.POST['country']
#     address= request.POST['address']
#     facebook= request.POST['facebook']
#     job= request.POST['job']
#     phone= request.POST['phone']
#     twitter= request.POST['twitter']
#     instagram= request.POST['instagram']
#     linkedin= request.POST['linkedin']
#     lastname=request.POST['lastname']
#     email=request.POST['email']
#     namefirst=request.POST['namefirst']
    
    
    # user = User.objects.filter(username = email)
    
    # # user.firstName = firstname
    # # user.lastName = lastname
    # # user.email = email
    
    # Editprofile(
    # namefirst=namefirst,
    # lastname=lastname,
    # email=email,
    # profileimage=profileimage, 
    # about= about,
    # country= country,
    # address= address,
    # facebook= facebook,
    # job= job,
    # phone= phone,
    # twitter= twitter,
    # instagram= instagram,
    # linkedin= linkedin,
    # )
     return render(request, "userprofile.html")