from multiprocessing.context import AuthenticationError
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from booking.models import Room, Booking
from django.http import HttpResponse
from datetime import datetime
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from auth_system.forms import CustomUserCreationForm
from django.contrib.auth import logout


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
        # else:
        #     messages.error(request, "some error")
    else:
        form = CustomUserCreationForm()
        messages.error(request, "some error")

    return render(
        request,
        template_name="auth_system/register.html",
        context={"form": form},
    )

def logout_view(request):
    logout(request)
    return redirect("index")

# def login(request):
#     if request.method == "POST":
#         form = AuthenticationForm(request, date=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get("username")
#             password = form.cleaned_data.get("password")
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect("index")
#             else:
#                 messages.error(request, "неправильний логін та пароль")

# from .forms import CustomUser
#
# def register(request):
#     if request.method == "POST":
#         form = CustomUser(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect("index")
#     else:
#         form = CustomUser()
#     return render(request, "auth_system/register.html", {"form": form})
