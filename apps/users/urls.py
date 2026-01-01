from django.urls import path

from apps.users import views

urlpatterns = [
    path('accounts/register/', views.register, name="register"),
    path('accounts/login/', views.login, name="login"),
    path('accounts/logout/', views.register, name="logout"),
]
