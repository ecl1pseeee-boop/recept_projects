from django.urls import path

from apps.ingredients.views import IngredientCreateView

urlpatterns = [
    path('ingredient/create/', IngredientCreateView.as_view(), name="ingredient_create"),
]