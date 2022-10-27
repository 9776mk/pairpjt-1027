import re
from django.shortcuts import render, redirect

from accounts.forms import SignupForm, UpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout

from accounts.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

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
        if form.is_valid():
            form.save()
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

def follow(request, pk):
    user = User.objects.get(pk=pk)
    me = request.user
    if user in me.followings.all():
        me.followings.remove(user)
    else:
        me.followings.add(user)
    return redirect('accounts:detail', pk)