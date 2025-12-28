import os

import requests
from django.contrib.auth.models import User

from recepts.apps.recipes.models import Recipe

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.spoonacular.com"


# API запрос на получение number рецептов
def fetch_recipes(number = 5):
    SEARCH_URL = f"{BASE_URL}/recipes/complexSearch"
    params = {
        'apiKey': API_KEY,
        'number': number,
        'instructionsRequired': True,
        'addRecipeInformation': True
    }
    response = requests.get(SEARCH_URL, params=params)
    if response.status_code != 200:
        print("Error fetching recipes")
        return
    data = response.json()
    return data.get("results", [])


def set_difficulty(cooking_time: int, servings: int):
    if cooking_time >= 60 or servings >= 10:
        return 'hard'
    if 20 < cooking_time < 60 or 5 < servings < 10:
        return 'medium'
    return 'easy'

def get_instructions(recipe):
    instructions = ""
    analyzed = recipe.get("analyzedInstructions", [])
    if analyzed and isinstance(analyzed, list) and len(analyzed) > 0:
        steps = analyzed[0].get("steps", [])
        instructions = "\n".join(step.get("step", "") for step in steps)
    return instructions

# Сохрание рецептов в базу данных
def save_recipes(data):
    user = User.objects.first()
    for recipe in data:
        cooking_time = recipe.get("readyInMinutes", 0)
        servings = recipe.get("servings", 0)
        instructions = get_instructions(recipe)
        Recipe.objects.update_or_create(
            title = recipe.get("title"),
            description = recipe.get("summary"),
            image_url = recipe.get("image"),
            cooking_time = cooking_time,
            prep_time =  recipe.get("preparationMinutes", None),
            servings = servings,
            difficulty = set_difficulty(cooking_time, servings),
            user = user,
            instructions = instructions,
            source = recipe.get("sourceUrl"),
            external_id = recipe.get("id"),
        )

# Сохранение ингридиента в базу данных
def save_ingredient():
    pass

if __name__ == "__main__":
    info = fetch_recipes()
    save_recipes(info)