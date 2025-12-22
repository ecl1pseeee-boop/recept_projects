from django import forms

from recipes.models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'cooking-time', 'image', 'category', 'description', 'ingredients']
        widgets = {
            'category': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
            'ingredients': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
        }
        labels = {
            'category' : 'Выберите категорию',
            'ingredients' : 'Выберите ингридиенты'
        }