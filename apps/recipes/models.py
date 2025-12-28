from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Recipe(models.Model):
    DIFFICULTY_VALUES = [
        ('easy', 'Легкий'),
        ('medium', 'Средний'),
        ('hard', 'Сложный')
    ]

    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание рецепта")
    image_url = models.ImageField(upload_to="recipe_images/", blank=True, null=True, verbose_name="Изображение")
    cooking_time = models.PositiveIntegerField(help_text="Время приготовления в минутах", verbose_name="Время готовки")
    prep_time = models.PositiveIntegerField(blank=True, null=True, verbose_name="Время подготовки")
    servings = models.PositiveIntegerField(blank=True, null=True, verbose_name="Порции")
    difficulty = models.CharField(null=True, blank=True, choices=DIFFICULTY_VALUES, verbose_name="Уровень сложности")
    instructions = models.TextField(blank=True, null=True, verbose_name="Инструкции")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    # API spoonacular/user
    source = models.CharField(max_length=100, blank=True, null=True, verbose_name="Источник")
    external_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="Внешний ID")

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
