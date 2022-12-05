from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect

from .forms import *
from .models import *


def index(request):
    return render(request, 'cvmaker/index.html')


@login_required
def panel(request):
    jobseekers = JobSeeker.objects.all()
    return render(request, 'cvmaker/panel.html', {'jobseekers': jobseekers})


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(request,
                                username=form.cleaned_data['username'],
                                password=form.cleaned_data['password']
                                )

            if user is not None:
                if user.is_active:
                    auth_login(request, user)

                    return redirect('account:panel')
                else:
                    return redirect('account:index')
        else:
            return render(request, 'cvmaker/login.html', {'form': form})
    else:
        form = LoginForm()

    return render(request, 'cvmaker/login.html', {'form': form})


@login_required
def logout(request):
    auth_logout(request)
    return redirect('account:index')
