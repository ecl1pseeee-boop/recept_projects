from django.urls import path

from apps.favorites.views import FavoritesView, ToggleFavorite

urlpatterns = [
    path('accounts/profile/favorites/', FavoritesView.as_view(), name="user_favorites_recipes"),
    path('recipes/<int:pk>/favourite/', ToggleFavorite.as_view(), name="toggle_favorite"),
]
