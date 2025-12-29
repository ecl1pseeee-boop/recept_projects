from django.contrib import admin
from .models import Recipe, Category, RecipeCategory, RecipeIngredient

admin.site.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'external_id', 'user', 'created_at')
    search_fields = ('title', 'external_id')
admin.site.register(Category)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeCategory)