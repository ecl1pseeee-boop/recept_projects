from django import forms
from .models import Recipe, Category


class RecipeForm(forms.ModelForm):
    image_url = forms.URLField(required=False)

    class Meta:
        model = Recipe
        fields = ["title", "description", "image_url", "cooking_time", "prep_time", "servings", "difficulty", "instructions"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "w-full p-2 border rounded-lg"}),
            "description": forms.Textarea(attrs={"rows": 3, "class": "w-full p-2 border rounded-lg"}),
            "image_url": forms.URLInput(attrs={"class": "w-full p-2 border rounded-lg", "placeholder": "https://..."}),
            "cooking_time": forms.NumberInput(attrs={"min": 0, "class": "w-full p-2 border rounded-lg"}),
            "prep_time": forms.NumberInput(attrs={"min": 0, "class": "w-full p-2 border rounded-lg"}),
            "servings": forms.NumberInput(attrs={"min": 0, "class": "w-full p-2 border rounded-lg"}),
            "difficulty": forms.Select(attrs={"class": "w-full p-2 border rounded-lg"}),
            "instructions": forms.Textarea(attrs={"rows": 6, "class": "w-full p-2 border rounded-lg"}),
        }


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

    sort = forms.ChoiceField(required=False, choices=[
        ("", "Default"),
        ("new", "Newest"),
        ("old", "Oldest"),
        ("time_asc", "Cooking time (asc)"),
        ("time_desc", "Cooking time (desc)"),
        ("title_asc", "Title (A–Z)"),
        ("title_desc", "Title (Z–A)"),
    ])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.all()
