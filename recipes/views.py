from django.http import HttpRequest
from django.shortcuts import render

from recipes.models import Recipe


def home(request: HttpRequest):
    return render(request, 'home.html')

def receipt_list(request: HttpRequest):
    recipes = Recipe.objects.all()
    return render(request, 'all_recipes.html', {'recipes': recipes})

def create_recipe(request: HttpRequest):
    pass
