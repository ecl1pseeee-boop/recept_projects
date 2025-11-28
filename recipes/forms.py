from django import forms

from recipes.models import Recipe, Category, Ingredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'cooking_time', 'image', 'category', 'description']
        widgets = {
            'category': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
        }
        labels = {
            'category' : 'Выберите категорию',
        }