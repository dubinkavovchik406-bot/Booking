from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from django.utils.translation import gettext as _

from my_auth.forms import CustomUserCreationForm

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home-page')
    else:
        form = CustomUserCreationForm()

    context = {
        "form": form
    }

    return render(request=request, template_name="my_auth/register.html", context=context)

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home-page")
        else:
            messages.error(request=request, message=_("Incorrect username or password"))
    else:
        form = AuthenticationForm()

    context = {
        "form": form
    }

    return render(request=request, template_name="my_auth/login.html", context=context)

def user_logout(request):
    logout(request=request)
    return redirect("home-page")