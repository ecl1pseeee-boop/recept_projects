from django.http import HttpRequest
from django.shortcuts import render

from .forms import RecipeForm
from .models import Recipe


def home(request: HttpRequest):
    return render(request, 'home.html')

def receipt_list(request: HttpRequest):
    recipes = Recipe.objects.all()
    return render(request, 'all_recipes.html', {'recipes': recipes})

def create_recipe(request: HttpRequest):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = RecipeForm()

    return render(request, 'includes/create-recipe-block.html', {'form': form})

