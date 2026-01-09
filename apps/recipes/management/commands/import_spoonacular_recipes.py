import os
import requests
import logging
from django.core.management import BaseCommand

from apps.recipes.services.spoonacular_importer import SpoonacularImporter

API_KEY = os.getenv("API_KEY")
SPOONACULAR_URL = os.getenv("SPOONACULAR_URL")
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Импортирует рецепты из SPOONACULAR"

    def add_arguments(self, parser):
        parser.add_argument('--query', type=str, help="Поисковый запрос")
        parser.add_argument('--number', type=int, default=5, help="Количество рецептов (максимально 100)")

    def handle(self, *args, **options):
        data = self.fetch_recipes_by_number(
            query=options["query"],
            number=min(options["number"], 100)
        )
        importer = SpoonacularImporter()
        importer.import_recipes(data)

        self.stdout.write(self.style.SUCCESS(f"Успешно импортировано {len(data)} рецептов"))

    @staticmethod
    def fetch_recipes_by_number(query=None, number=1):
        """
        Ищет некоторое количество рецептов на Spoonacular .
        Возвращает список рецептов в формате:
        {
            "offset": 0,
            "number": 1,
            "results": [
                {
                    "id": 716429,
                    "title": "Pasta with Garlic, Scallions, Cauliflower & Breadcrumbs",
                    "image": "https://img.spoonacular.com/recipes/716429-312x231.jpg",
                    "imageType": "jpg",
                }
            ],
            "totalResults": 86
        }
        """
        SEARCH_URL = f"{SPOONACULAR_URL}/recipes/complexSearch"
        params = {
            'apiKey': API_KEY,
            'number': number,
            'instructionsRequired': True,
            'addRecipeInformation': True,
            'fillIngredients': True
        }
        if query:
            params['query'] = query

        try:
            response = requests.get(SEARCH_URL, params=params, timeout=10)
            response.raise_for_status()
            return response.json().get("results", [])
        except requests.exceptions.RequestException as e:
            logger.info(f"Ошибка получения рецептов: {e}")
            return []


