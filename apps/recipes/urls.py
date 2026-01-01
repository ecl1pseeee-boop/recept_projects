from django.urls import path
from .views import RecipeListView, HomeView, RecipeCreateView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('recipes/', RecipeListView.as_view(), name="recipe_list"),
    path('recipes/create/', RecipeCreateView.as_view(), name="recipe_create"),
]
