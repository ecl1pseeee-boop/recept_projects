from django.contrib import admin
from .models import Recipe, Category, RecipeCategory, RecipeIngredient

admin.site.register(Recipe)
admin.site.register(Category)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeCategory)