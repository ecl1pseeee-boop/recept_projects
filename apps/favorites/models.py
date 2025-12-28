from django.db import models
from DjangoUlearn import settings
from apps.recipes.models import Recipe


class UserFavorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')
        verbose_name = "Избранные"
        verbose_name_plural = "Избранные"

    def __str__(self):
        return f'{self.user.username} - {self.recipe.title}'