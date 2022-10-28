import re
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from accounts.forms import ProfileForm, SignupForm, UpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout

from accounts.models import Profile, User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    user = User.objects.all()
    context = {
        'user' : user,
    }
    return render(request, "accounts/index.html", context)

def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    if request.method=='POST':
        form = SignupForm(request.POST)
        profile = Profile()
        if form.is_valid():
            user = form.save()
            profile.user = user
            profile.save()
            return redirect('accounts:index')

    else:
        form = SignupForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/signup.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'accounts:index')
    else:
        form = AuthenticationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('accounts:index')

def detail(request, pk):
    user = User.objects.get(pk=pk)
    context = {
        'user' : user,
    }
    return render(request, 'accounts/detail.html', context)

def update(request):
    if request.method=='POST':
        form = UpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:detail', request.user.pk)
    else:
        form = UpdateForm(instance=request.user)
    context = {
        'form' : form,
    }
    return render(request, 'accounts/update.html', context)

def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('accounts:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form' : form,
    }
    return render(request, 'accounts/password.html', context)

def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('accounts:index')

@login_required
def follow(request, pk):
    if request.user.is_authenticated:
        user = User.objects.get(pk=pk)
        me = request.user
        if me != user:
            if user.followers.filter(pk=me.pk).exists():
                user.followers.remove(me)
                is_followed = False
            else:
                user.followers.add(me)
                is_followed = True
            context = {
                'is_followed' : is_followed,
                'followersC' : user.followers.count(),
                'followingsC' : user.followings.count(),
            }
            return JsonResponse(context)
        return redirect('accounts:detail', pk)
    return redirect('accounts:login')

def profile(request, pk):
    user = get_user_model().objects.get(pk=pk)
    if request.method=='POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:detail', pk)
    else:
        form = ProfileForm(instance=request.user.profile)
    context = {
        'user' : user,
        'form' : form,
    }
    return render(request, 'accounts/profile.html', context)