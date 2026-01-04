from django import forms
from django.forms.models import inlineformset_factory

from .models import Recipe, Category, RecipeCategory, RecipeIngredient


class RecipeForm(forms.ModelForm):
    image_url = forms.URLField(required=False)
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.SelectMultiple(
            attrs={
                "class": "w-full p-2 border rounded-lg",}),
        label="Categories")

    class Meta:
        model = Recipe
        fields = ["title", "description", "image_url",
                  "cooking_time", "prep_time", "servings",
                  "difficulty", "instructions"]
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


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        base = (
            "w-full px-3 py-2.5 rounded-xl "
            "border border-gray-300 dark:border-gray-600 "
            "bg-white dark:bg-gray-700 text-gray-900 dark:text-white "
            "placeholder:text-gray-400 dark:placeholder:text-gray-500 "
            "focus:outline-none focus:ring-2 focus:ring-indigo-500"
        )

        for field in self.fields.values():
            field.widget.attrs["class"] = base

        self.fields["categories"].widget.attrs["class"] = base

        if self.instance and self.instance.pk:
            self.fields["categories"].initial = Category.objects.filter(recipecategory__recipe=self.instance)


    def save(self, commit=True):
        recipe = super().save(commit=commit)
        selected_categories = self.cleaned_data.get("categories", [])

        if not recipe.pk:
            return recipe

        RecipeCategory.objects.filter(recipe=recipe).delete()
        RecipeCategory.objects.bulk_create(
            [RecipeCategory(recipe=recipe, category=cat)
             for cat in selected_categories])
        return recipe

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ["ingredient", "quantity", "unit", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base = (
            "w-full px-3 py-2.5 rounded-xl "
            "border border-gray-300 dark:border-gray-600 "
            "bg-white dark:bg-gray-700 text-gray-900 dark:text-white "
            "placeholder:text-gray-400 dark:placeholder:text-gray-500 "
            "focus:outline-none focus:ring-2 focus:ring-indigo-500"
        )

        for name, field in self.fields.items():
            field.widget.attrs["class"] = base

        if "description" in self.fields:
            self.fields["description"].widget.attrs.update({"rows": 2})

RecipeIngredientFormSet = inlineformset_factory(
    parent_model=Recipe,
    model=RecipeIngredient,
    form = RecipeIngredientForm,
    fields=("ingredient", "quantity", "unit", "description"),
    extra=1,
    can_delete=True,
)

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

class RecipeUpdateForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "description", "image_url", "cooking_time", "prep_time", "servings", "difficulty",
                  "instructions"]
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
