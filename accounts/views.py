from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout

def user_register(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if password == cpassword:
            validate_password(password)
            User.objects.create_user(fullname=fullname,username=username,email=email,phone=phone,password=password)
            return redirect("signup")
        else:
            messages.error(request,'password and c password not matched')
            return redirect("signup")
            

    return render(request, 'account.html')

def log_in(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            messages.error(request, "user name not registered")
        else:
            user= authenticate(request,username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    return render(request, 'account.html')




