from django.contrib import admin

from recipes.models import Recipe, Category, Ingredient

admin.site.register(Recipe)
admin.site.register(Category)
admin.site.register(Ingredient)
# Register your models here.
