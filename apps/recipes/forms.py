from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'image_url', 'cooking_time', 'prep_time', 'servings', 'difficulty', 'instructions']