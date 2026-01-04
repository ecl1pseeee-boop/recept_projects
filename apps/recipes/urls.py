from django.urls import path
from .views import RecipeListView, RecipeCreateView, RecipeDetailView, UserRecipeListView, RecipeUpdateView, \
    RecipeDeleteView

urlpatterns = [
    path("recipes/", RecipeListView.as_view(), name="recipe_list"),
    path("recipes/create/", RecipeCreateView.as_view(), name="recipe_create"),
    path("recipes/<int:pk>/", RecipeDetailView.as_view(), name="recipe_detail"),
    path("recipes/<int:pk>/edit/", RecipeUpdateView.as_view(), name="recipe_update"),
    path("recipes/<int:pk>/delete/", RecipeDeleteView.as_view(), name="recipe_delete"),
    path("accounts/profile/recipes", UserRecipeListView.as_view(), name="user_recipes"),
]
