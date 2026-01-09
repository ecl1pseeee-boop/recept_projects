from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from apps.ingredients.models import Ingredient


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название", unique=True)
    slug = models.SlugField()

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Recipe(models.Model):
    DIFFICULTY_VALUES = [
        ('easy', 'Легкий'),
        ('medium', 'Средний'),
        ('hard', 'Сложный')
    ]

    title = models.CharField(max_length=100, verbose_name="Title")
    description = models.TextField(blank=True, null=True, verbose_name="Recipe Description")
    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Image URL")
    image = models.ImageField(upload_to="images/", blank=True, null=True, verbose_name="Uploaded Image")
    cooking_time = models.PositiveIntegerField(help_text="Cooking time in minutes", verbose_name="Cooking time")
    prep_time = models.PositiveIntegerField(blank=True, null=True, verbose_name="Preparation time in minutes")
    servings = models.PositiveIntegerField(blank=True, null=True, verbose_name="Servings")
    difficulty = models.CharField(null=True, blank=True, choices=DIFFICULTY_VALUES, verbose_name="Difficulty level")
    instructions = models.TextField(blank=True, null=True, verbose_name="Instructions")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Recipe Autor", null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Creation time")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update time")

    # API spoonacular/user
    source = models.CharField(max_length=100, blank=True, null=True, verbose_name="Source")
    external_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="External ID", unique=True)

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("recipe_detail", args={"pk": self.pk})

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=50, blank=True)  # например: "pcs", "g", "ml" или пусто
    description = models.CharField(
        max_length=255,
        blank=True,
        help_text="Дополнительное уточнение: 'средние', 'натёртый', 'нарезанный кубиками' и т.д."
    )

    class Meta:
        unique_together = ('recipe', 'ingredient')
        verbose_name = "Ингридиент в рецепте"
        verbose_name_plural = "Ингридиенты в рецепте"

    def __str__(self):
        return self.ingredient.name

class RecipeCategory(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Категория рецепта"
        verbose_name_plural = "Категории рецептов"

    def __str__(self):
        return f"{self.category.name} - {self.recipe.title}"