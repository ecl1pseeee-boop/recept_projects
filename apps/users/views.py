from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm

def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

            messages.success(request, "Аккаунт создан! Добро пожаловать 🙂")
            return redirect("home")
        else:
            messages.error(request, f"В форме есть ошибки: {form.errors} ")
    else:
        form = UserRegistrationForm()
    return render(request, "users/register.html", {"form": form})

