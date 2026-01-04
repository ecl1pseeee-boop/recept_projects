from django import forms

from apps.ingredients.models import Ingredient


class IngredientCreateForm(forms.ModelForm):
    name = forms.CharField(
        max_length=10,
        required=True,
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    image = forms.ImageField(
        required=False,
        label='Аватар',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Ingredient
        fields = ["name", "image"]

    def save(self, commit=True):
        ingredient = super().save(commit=False)
        ingredient.name = self.cleaned_data["name"]
        image = self.cleaned_data["image"]

        if commit:
            ingredient, created = Ingredient.objects.get_or_create(
                name=ingredient.name,
            )
            ingredient.image = image if image else None
            ingredient.save()

        return ingredient