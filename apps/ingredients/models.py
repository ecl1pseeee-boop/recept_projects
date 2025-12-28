from django.db import models
from DjangoUlearn import settings


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="ingredient_images/", blank=True, null=True)

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return f"{self.name}"

class UserIngredient(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pantry")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='in_pantry_of')
    quantity = models.FloatField(help_text="Количество (например, 500)")
    unit = models.CharField(max_length=50, help_text="Единица измерения (г, мл, шт и т.д.)")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'ingredient')
        verbose_name = "User Ingredient"
        verbose_name_plural = "User Ingredients"