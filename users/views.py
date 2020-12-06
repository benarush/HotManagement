from django.shortcuts import render , redirect
import os
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm , UserUpdateForm , ProfileUpdateForm
from blog.models import Post
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()     # Save the Details in the DB
            username = form.cleaned_data.get("username")
            messages.success(request , "User {} Created! , Now You Able to Login !".format(username))
            return redirect('login')
        else:
            messages.warning(request, "User registration failed - Whats Wrong Dude?")
    else:
        form = UserRegisterForm()
    return render(request,"users/register.html" , {'form':form , 'latest_post':Post.objects.last()})


@login_required
def profile(request):
    if request.method == 'POST':
        oldImage = request.user.profile.image.path
        oldGender = request.user.profile.gender
#       we give here two variable for the class. first request.POST that hold the insert data from user , and
#       the instance the define that we want to UPDATE the request.user data .
        user_form = UserUpdateForm(request.POST , instance=request.user)
#       Here its the same , but we need to add request.FILES becues we dealing with files...
        profile_form = ProfileUpdateForm(request.POST , request.FILES ,instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            # Remove the Older Photo
            print("old : {} \nsecond:{}".format(oldImage,request.user.profile.image.path))
            if "default\\" not in oldImage and oldImage != request.user.profile.image.path:
                try:
                    os.remove(oldImage)
                except:
                    print("There is no photo for user {} , even no defult".format(request.user.username))
            elif "default\\" in oldImage and oldGender != request.user.profile.gender:
                print("Old Gender : {} , And New: {}".format(oldGender , request.user.profile.gender))
                profile_form = profile_form.save(commit=False)
                if request.user.profile.gender=='female':
                    profile_form.image = 'profile_pics/default/Girl_default.png'
                else:
                    profile_form.image = 'profile_pics/default/Male_default.png'
            user_form.save()
            profile_form.save()
            messages.success(request , "Updating Success!")
            return redirect('profile')
        else:
            messages.warning(request, "User registration failed - Whats Wrong Dude?")
    else:
        # Here the instance= will add the data to the fields...
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context ={
        'user_form'     : user_form ,
        'profile_form'  : profile_form,
        'latest_post': Post.objects.last()
    }
    return render(request , "users/profile.html" , context )