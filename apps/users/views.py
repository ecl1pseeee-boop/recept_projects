from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .forms import UserRegistrationForm, ProfileUpdateForm, UserUpdateForm
from .models import Profile

# TODO: Переделать через CLASS-BASED
def user_register(request):
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


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True

class ProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.method == "POST":
            context["user_form"] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context["user_form"] = UserUpdateForm(instance=self.request.user)

        return context

    def form_valid(self, form):
        user_form = UserUpdateForm(self.request.POST, instance=self.request.user)

        if user_form.is_valid():
            user_form.save()
            return super().form_valid(form)

        return self.form_invalid(form)