from django.db import models

from apps.recipes.models import Recipe


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
    image = models.ImageField(upload_to="ingredient_images/", blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    measurement = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.measurement}"