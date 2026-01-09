import logging

from django.contrib.auth.models import User
from django.db import transaction

from apps.ingredients.models import Ingredient
from apps.recipes.models import RecipeCategory, RecipeIngredient, Recipe, Category

logger = logging.getLogger(__name__)

class SpoonacularImporter:
    def __init__(self, user = None):
        self.user = user or self.get_spoonacular_user()

    @staticmethod
    def get_spoonacular_user():
        user, created = User.objects.get_or_create(
            username='spoonacular_importer',
            defaults={
                'email': 'spoonacular@example.com',
                'is_active': False,
            }
        )
        user.set_unusable_password()
        user.save()
        return user

    def import_recipes(self, data):
        """
        Сохраняет всю полученную информацию из API
        """
        if not data:
            logger.info("Нет данных для сохранения")
            return

        recipes = []
        for recipe_data in data:
            try:
                with transaction.atomic():
                    recipe = self.save_recipe_info(recipe_data)
                    recipes.append(recipe)
            except Exception as e:
                logger.info(f"Ошибка сохранения рецепта: {e}")
                continue

        return recipes


    def save_recipe_info(self, recipe_data):
        recipe = self.save_recipe(self.user, recipe_data) # Таблица Recipe
        categories = self.save_categories(recipe_data.get("dishTypes", [])) # Таблица Categories
        self.save_recipe_categories(recipe, categories) # Таблица Recipe_Categories
        self.save_recipe_ingredients(recipe, recipe_data.get("extendedIngredients", [])) # Таблица Recipe_Ingredients
        logger.info(f"Рецепт {recipe.title} сохранён")
        return recipe

    def save_recipe_ingredients(self, recipe, ingredients):
        for ingredient_data in ingredients:
            ingredient = self.save_ingredient(ingredient_data)
            if ingredient:
                self.save_recipe_ingredient(recipe, ingredient, ingredient_data)
            else:
                logger.warning(f"Не удалось сохранить ингредиент для рецепта {recipe.title}")

    def save_ingredient(self, ingredient_data):
        """
        Сохраняет ингридиент
        """
        if not ingredient_data:
            logger.info("Ингридиент без названия")
            return None

        name = ingredient_data.get("name", "").strip()
        name = self.clean_ingredient_name(name)

        image = ingredient_data.get("image", "").strip()
        if image and not image.startswith("http"):
            image = f"https://spoonacular.com/cdn/ingredients_100x100/{image}"

        ingredient, created = Ingredient.objects.get_or_create(
            name=name,
            defaults={'image': image}
        )

        return ingredient

    @staticmethod
    def save_recipe_ingredient(recipe, ingredient, ingredient_data):
        """
        Сохраняет связь рецепта и ингридиента
        """
        RecipeIngredient.objects.update_or_create(
            recipe=recipe,
            ingredient=ingredient,
            defaults={
                'quantity': ingredient_data.get("amount") or 0,
                'unit': ingredient_data.get("unit", "")[:50],
                'description': (ingredient_data.get("original", "") or "")[:200],
            }
        )

    @staticmethod
    def clean_ingredient_name(name):
        """
        Очищает название ингредиента
        """
        import re
        name = re.sub(r'\([^)]*\)', '', name)
        name = ' '.join(name.split())
        return name.strip().title()


    def save_recipe(self, user, recipe):
        """
        Сохраняет рецепт
        """
        title = recipe.get("title")
        if not title:
            title = "Рецепт без названия"

        cooking_time = recipe.get("readyInMinutes", 0)
        servings = recipe.get("servings", 0)
        instructions = self.get_instructions(recipe)

        recipe_id = recipe.get("id")
        if not recipe_id:
            logger.warning(f"Пропущен рецепт без ID: {recipe.get('title')}")
            return None


        recipe, created = Recipe.objects.update_or_create(
            external_id=recipe_id,
            defaults={
                'title': title,
                'description': self.clean_html(recipe.get("summary", "")),
                'image_url': recipe.get("image", "").strip(),
                'cooking_time': cooking_time,
                'prep_time': recipe.get("preparationMinutes"),
                'servings': servings,
                'difficulty': self.set_difficulty(cooking_time, servings),
                'user': user,
                'instructions': instructions,
                'source': recipe.get("sourceUrl", ""),
            }
        )

        if created:
            logger.info(f"Новый рецепт '{recipe.title}' создан")
        else:
            logger.info(f"Рецепт '{recipe.title}' обновлен")
        return recipe

    @staticmethod
    def set_difficulty(cooking_time: int, servings: int):
        """
        Рассчитывает сложность рецепта
        """
        if cooking_time >= 60 or servings >= 10:
            return 'hard'
        if 20 < cooking_time < 60 or 5 < servings < 10:
            return 'medium'
        return 'easy'

    @staticmethod
    def clean_html( text):
        """
        Очищает HTML теги из текста
        """

        if not text:
            return ""

        import re
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    @staticmethod
    def get_instructions( recipe):
        """
        Извлекает инструкции из данных рецепта
        """
        instructions = ""
        analyzed = recipe.get("analyzedInstructions", [])
        if analyzed and isinstance(analyzed, list) and len(analyzed) > 0:
            steps = analyzed[0].get("steps", [])
            instructions = "\n".join(step.get("step", "") for step in steps)
        return instructions

    @staticmethod
    def save_categories(dish_types):
        categories = []
        for category in dish_types:
            if not category:
                continue

            category_name = str(category).strip().title()
            if not category_name:
                continue

            category, created = Category.objects.get_or_create(
                name=category_name,
            )

            if created:
                logger.info(f"Категория {category_name} создана")
            else:
                logger.info(f"Категория {category_name} обновлена")

            categories.append(category)
        return categories

    @staticmethod
    def save_recipe_categories(recipe, categories):
        """
        Сохраняет рецепт и его категорию в отдельную таблицу
        """
        for category in categories:
            relation, created = RecipeCategory.objects.get_or_create(
                recipe=recipe,
                category=category,
            )
            if created:
                logger.info(f"Создана связь: {recipe.title} - {category.name}")
            else:
                logger.info(f"Обновлена связь: {recipe.title} - {category.name}")