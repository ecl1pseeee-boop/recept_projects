from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

from apps.categories.models import Category


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    cooking_time = models.PositiveIntegerField(help_text="Время приготовления в минутах")
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="recipe_images/",  blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    description = models.TextField(blank=True, null=True, verbose_name="Описание рецепта")

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ['-created_at']


    def save(self, *args, **kwargs):
        if not self.slug:
            main_slug = slugify(self.title) # основа
            slug = main_slug # с добалвение counter
            counter = 1
            while Recipe.objects.filter(slug=slug).exclude(pk = self.pk).exists():
                slug = f"{main_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
