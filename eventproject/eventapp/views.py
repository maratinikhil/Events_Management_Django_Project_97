from django.shortcuts import render,redirect
from django.contrib import messages
from eventapp.models import User
from django.core.mail import send_mail
from django.contrib.auth import login as auth_login, logout as auth_logout
import random

def home(request):
    return render(request,"home.html")

def signup(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')   
        mobile = request.POST.get('mobile')   
        password = request.POST.get('password')   
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request,'Passwords do not match!')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request,"Email already registered")
            return redirect('signup')
        
        if User.objects.filter(mobile=mobile).exists():
            messages.error(request,"Mobile number already registered")
            return redirect('signup')
        
        User.objects.create(
            firstname = firstname,
            lastname = lastname,
            email = email,
            mobile = mobile,
            password = password,
        )

        messages.success(request,"registration success! Please log in")
        return redirect('login')
    return render(request,'signup.html')

def login(request):
    if request.method == "POST":
        user_input = request.POST.get('user_input')
        user=None
        email_to_send=None

        if '@' in user_input:
            try:
                user = User.objects.get(email=user_input)
                email_to_send=user.email
            except User.DoesNotExist:
                messages.error(request,'Email not registered')
                return redirect('login')
        
        else:
            try:
                user = User.objects.get(mobile=user_input)
                email_to_send = user.email
            except User.DoesNotExist:
                messages.error(request,"Mobile not registered")
                return redirect("login")
            
        otp = random.randint(100000,999999)
        request.session["otp"] = otp
        request.session["user_id"] = user.id

        send_mail(
            subject="Your Login OTP",
            message=f"Your OTP is:{otp}",
            from_email="yourgmail@gmail.com",
            recipient_list=[email_to_send],
            fail_silently=False
        )

        messages.error(request,"OTP sent to your email")

        return redirect("login_otp_verify")
    
    return render(request,"login.html")


def login_otp_verify(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")

        if str(request.session.get('otp')) == entered_otp:
            return redirect("login_password")
        else:
            messages.error(request,"Invalid OTP!")
            return redirect("login_otp_verify")
    
    return render(request,"login_otp_verify.html")



def login_password(request):
    if request.method == "POST":
        password = request.POST.get("password")
        user = User.objects.get(id=request.session["user_id"])

        if user.password == password:
            request.session['user_authenticated'] = True
            request.session['user_name'] = user.firstname
            # messages.error(request, f"Welcome {user.firstname}")
            return redirect("home")
        else:
            messages.error(request,"Incorrect password!")
            return redirect("login_password")
    return render(request,"login_password.html")

def logout(request):
    request.session.flush()
    return redirect('login')

