from django.shortcuts import render ,redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import authenticate, login
from userauths.models import Profile
from django.contrib import messages


def RegisterView(request, *args, **kwargs):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey {request.user.username}, you are already logged in")
        return render(request, "core:index") 

    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        full_name = form.cleaned_data.get('full_name')
        phone = form.cleaned_data.get('phone')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')

        user = authenticate(email=email, password=password)
        login(request, user)

        messages.success(request, f"Hi {request.user.username}, your account have been created successfully.")

        profile = Profile.objects.get(user=request.user)
        profile.full_name = full_name
        profile.phone = phone
        profile.save()

        return render(request, "core:index") 
    
    context = {'form':form}
    return render(request, 'userauths/sign-up.html', context)
