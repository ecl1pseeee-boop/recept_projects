from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView

from apps.ingredients.forms import IngredientCreateForm
from apps.ingredients.models import Ingredient


class IngredientListView(ListView):
    model = Ingredient
    context_object_name = "ingredients"




class IngredientDetailView(DetailView):
    model = Ingredient
    template_name = "ingredients/detail_ingredient.html"




class IngredientCreateView(CreateView):
    model = Ingredient
    form_class = IngredientCreateForm
    template_name = "ingredients/create_ingredient.html"

    def form_valid(self, form):
        ingredient = form.save(commit=False)
        ingredient.save()
        return super().form_valid(form)

    def get_success_url(self):
        pass
