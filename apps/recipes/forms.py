from django import forms

from .models import Recipe, Category


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'image_url', 'cooking_time', 'prep_time', 'servings', 'difficulty', 'instructions']

class RecipeFilterForm(forms.Form):
    search = forms.CharField(label='Search', max_length=100, required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.none(), required=False)
    servings = forms.IntegerField(required=False, min_value=0)
    source = forms.ChoiceField(required=False, choices=[
        ("", "Any"),
        ("user", "User"),
        ("spoonacular", "Spoonacular"),
    ])
    has_image = forms.BooleanField(required=False)
    freshness = forms.ChoiceField(required=False, choices=[
        ("", "Any"),
        ("week", "Last 7 days"),
        ("month", "Last 30 days"),
        ("half-year", "Last half year"),
        ("year", "Last year"),
    ])
    cooking_time = forms.IntegerField(required=False, min_value=0)
    prep_time = forms.IntegerField(required=False, min_value=0)
    difficulty = forms.ChoiceField(required=False, choices=[("", "Any")] + Recipe.DIFFICULTY_VALUES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.all()
