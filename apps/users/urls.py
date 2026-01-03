from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from apps.users import views
from apps.users.views import CustomLoginView, ProfileView

urlpatterns = [
    path('accounts/register/', views.user_register, name="register"),
    path('accounts/login/', CustomLoginView.as_view(), name="login"),
    path('accounts/logout/', LogoutView.as_view(), name="logout"),
    path('accounts/profile/', ProfileView.as_view(), name="profile"),
]
