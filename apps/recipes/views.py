from django.http import HttpRequest
from django.shortcuts import render
from django.db.models import Q

from .forms import RecipeForm
from .models import Recipe, Category


def home(request: HttpRequest):
    return render(request, 'home.html')

def recipe_list(request: HttpRequest):
    recipes = Recipe.objects.all()

    search = request.GET.get('search', '').strip()
    if search:
        recipes = recipes.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )

    context = {
        'recipes': recipes,
        'search_query': search,
        'categories': Category.objects.all(),
        'difficulty': Recipe.DIFFICULTY_VALUES,
    }
    if request.headers.get('HX-Request') == 'true':
        return render(request, 'includes/all_recipe_blocks.html', context)
    else:
        return render(request, 'all_recipes.html', context)


def create_recipe(request: HttpRequest):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = RecipeForm()

    return render(request, 'includes/create-recipe-block.html', {'form': form})

