import os
import requests

from apps.recipes.services.spoonacular_importer import SpoonacularImporter

API_KEY = os.getenv("API_KEY")
SPOONACULAR_URL = os.getenv("SPOONACULAR_URL")

def get_recipes_by_ingredients(ingredients: str, number = 3):
    data = fetch_recipes_by_ingredients(number=number, ingredients=ingredients)
    return process_recipes(data)

def fetch_recipes_by_ingredients(number: int, ingredients: str):
    SEARCH_URL = f"{SPOONACULAR_URL}/recipes/findByIngredients"

    params = {
        'apiKey': API_KEY,
        'ingredients': ingredients,
        'number': number,
        'ranking': 1,
        'ignorePantry': True,
    }

    try:
        response = requests.get(SEARCH_URL, params=params, timeout=15)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return []

def fetch_recipe_by_id(recipe_id: int):
    SEARCH_URL = f"{SPOONACULAR_URL}/recipes/{recipe_id}/information"
    params = {"apiKey": API_KEY}

    try:
        response = requests.get(SEARCH_URL, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {}

def process_recipes(data):
    imported_recipes = []
    for recipe in data:
        recipe_id = recipe.get("id")
        if not recipe_id:
            continue

        recipe_data = process_recipe(recipe_id) # Импорт рецепта
        if recipe_data is None:
            continue

        missed_ingredients = get_ingredients(recipe, "missedIngredients") # Получаем недостающие ингридиенты
        used_ingredients = get_ingredients(recipe, "usedIngredients") # Получаем используемые ингридиенты
        unused_ingredients = get_ingredients(recipe, "unusedIngredients") # Получаем неиспользуемые ингридиенты

        imported_recipes.append({
            "recipe": recipe_data,
            "missed_ingredients": missed_ingredients,
            "used_ingredients": used_ingredients,
            "unused_ingredients": unused_ingredients
        })

    return imported_recipes

def process_recipe(recipe_id: int):
    recipe_data = fetch_recipe_by_id(recipe_id)
    if not recipe_data:
        return None
    recipe_importer = SpoonacularImporter()
    recipe = recipe_importer.save_recipe_info(recipe_data)
    return recipe

def get_ingredients(recipe, ingredient_type: str):
    missed_ingredients = recipe.get(ingredient_type, [])
    ingredients_name = []
    for ingredient in missed_ingredients:
        ingredient_name = ingredient.get("name")
        if ingredient_name:
            ingredients_name.append(ingredient_name)
    return ingredients_name