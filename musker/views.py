from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
# Create your views here.
from django.contrib.auth import login,logout,authenticate
from .forms import MeepForm,SignUpForm
from django.contrib.auth.models import User


def home(request):
    if request.user.is_authenticated:
        form=MeepForm(request.POST or None)
        if request.method=='POST':
            if form.is_valid():
                meep=form.save(commit=False)
                meep.user=request.user
                meep.save()
                messages.success(request,'Your Meep Has Been Posted')
                return redirect('home')

        meeps=Meep.objects.all().order_by('-created_at')
        return render(request,'home.html',{'meeps':meeps,'form':form})
    else:
        meeps=Meep.objects.all().order_by('-created_at')

        return render(request,'home.html',{'meeps':meeps})
        


def profile_list(request):
    if request.user.is_authenticated:
        profiles=Profile.objects.exclude(user=request.user)
        return render(request,'profiles.html',{'profiles':profiles})
    else:
        messages.success(request,'You must be logged in to View this page')
        return redirect('home')
    

def profile(request,pk):
    if request.user.is_authenticated:
        profile=Profile.objects.get(pk=pk)
        meeps=Meep.objects.filter(user_id=pk)
        if request.method=='POST':
            current_user=request.user.profile
            action=request.POST['follow']
            if action =='unfollow':
                current_user.follows.remove(profile)
            elif action=='follow':
                current_user.follows.add(profile)

            current_user.save()
        return render(request,'profile.html',{'profile':profile,'meeps':meeps})
    else:
        messages.success(request,'You must be logged in to View this page')
        return redirect('home')
    

def login_user(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        print(User.objects.get(username=username))
        if user is not None:
            login(request,user)
            messages.success(request,'You Have Been logged in successfully')
            return redirect('home')
        else:
            print("error=================================")
            messages.success(request,'There was an error logging in.')
            return redirect('login')
    else:  
        return render(request,'login.html',{})



def logout_user(request):
    logout(request)
    messages.success(request,'You have been logged out.')
    return redirect('login')


def register_user(request):
    form=SignUpForm()
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']            
            # first_name=form.cleaned_data['first_name']
            # last_name=form.cleaned_data['last_name']
            # email=form.cleaned_data['email']            
            # Login
            user=authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,'You are registered  successfully')
            return redirect('home')
    return render(request,'register.html',{'form':form}) 

def update_user(request):
    if request.user.is_authenticated:
        current_user=User.objects.get(id=request.user.id)
        form=SignUpForm(request.POST or None,instance=current_user)
        new_username = request.POST.get('username', '')
        if new_username != current_user.username:
            if User.objects.filter(username=new_username).exists():
                messages.error(request, 'Username is already taken.')
                return render(request, 'update_user.html', {'form': SignUpForm(instance=current_user)})

        form = SignUpForm(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Profile has been updated')
            return redirect('home')
        if form.is_valid():
            form.save()
            login(request,current_user)
            messages.success(request,'Your Profile has been updated')
            return redirect('home')
        return render(request,'update_user.html',{'form':form})
    else:
        messages.success(request,'You Must Be Logged In To View This')
        return redirect('home')
