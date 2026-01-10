import os
from datetime import timedelta

import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, FormView
from django.db.models import Q
from .forms import RecipeForm, RecipeFilterForm, RecipeUpdateForm, RecipeIngredientFormSet, IngredientSearchForm
from .models import Recipe, Category
from .services.import_by_ingredients import get_recipes_by_ingredients

API_KEY = os.getenv("API_KEY")
SPOONACULAR_URL = os.getenv("SPOONACULAR_URL")
COUNTER = 5

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "recipes/actions/recipe_creating.html"
    success_url = reverse_lazy("recipe_list")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.source = "user"
        self.object.save()

        form.instance = self.object
        form.save(commit=True)

        ingredients_formset = RecipeIngredientFormSet(
            self.request.POST, instance=self.object, prefix="ingredients"
        )

        if ingredients_formset.is_valid():
            ingredients_formset.save()
            return redirect(self.get_success_url())

        return self.render_to_response(self.get_context_data(form=form, ingredients_formset=ingredients_formset))

    def get_success_url(self):
        return reverse("recipe_detail", kwargs={"pk": self.object.pk})


    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.method == "POST":
            context["ingredients_formset"] = RecipeIngredientFormSet(self.request.POST, prefix="ingredients")
        else:
            context["ingredients_formset"] = RecipeIngredientFormSet(prefix="ingredients")
        return context

class RecipeListView(ListView):
    model = Recipe
    context_object_name = "recipes"
    template_name = "recipes/recipes_list_page.html"
    partial_template_name = "recipes/recipe_list.html"

    def get_filter_form(self) -> RecipeFilterForm:
        return RecipeFilterForm(self.request.GET)

    # TODO: Вынести фильтрацию
    def get_queryset(self):
        qs = super().get_queryset()
        form = self.get_filter_form()

        if not form.is_valid():
            return qs

        cd = form.cleaned_data

        search = cd["search"]
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        category=cd["category"]
        if category:
            qs = qs.filter(recipecategory__category=category).distinct()

        servings = cd["servings"]
        if servings is not None and servings != 0:
            qs = qs.filter(servings=servings)

        source = cd["source"]
        if source:
            qs = qs.filter(source=source)

        has_image = cd["has_image"]
        if has_image:
            qs = qs.filter(Q(image_url__isnull=False) | (Q(image__isnull=False) & ~Q(image_url="")))

        freshness = cd["freshness"]
        if freshness:
            mapping = {
                "week": 7,
                "month": 30,
                "half-year": 182,
                "year": 365,
            }
            days = mapping.get(freshness)
            if days:
                qs = qs.filter(created_at__gte=timezone.now() - timedelta(days=days))

        cooking_time = cd["cooking_time"]
        if cooking_time is not None:
            qs = qs.filter(cooking_time__lte=cooking_time)

        prep_time = cd["prep_time"]
        if prep_time is not None:
            qs = qs.filter(prep_time__lte=prep_time)

        difficulty = cd["difficulty"]
        if difficulty:
            qs = qs.filter(difficulty=difficulty)

        sort = cd.get("sort") or ""

        if sort == "new":
            qs = qs.order_by("-created_at")
        elif sort == "old":
            qs = qs.order_by("created_at")
        elif sort == "time_asc":
            qs = qs.order_by("cooking_time", "-created_at")
        elif sort == "time_desc":
            qs = qs.order_by("-cooking_time", "-created_at")
        elif sort == "title_asc":
            qs = qs.order_by("title")
        elif sort == "title_desc":
            qs = qs.order_by("-title")

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_filter_form()
        form.is_valid()
        cd = form.cleaned_data
        context["filter_form"] = form
        context["search_query"] = self.request.GET.get("search", "")
        context["categories"] = Category.objects.all()
        context["difficulty"] = Recipe.DIFFICULTY_VALUES
        context["selected_source"] = cd.get("source") or ""
        context["selected_difficulty"] = cd.get("difficulty") or ""
        context["selected_freshness"] = cd.get("freshness") or ""
        context["selected_has_image"] = bool(cd.get("has_image"))
        context["selected_servings"] = cd.get("servings")
        context["selected_category"] = cd.get("category")
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('HX-Request') == "true":
            self.template_name = self.partial_template_name
        return super().render_to_response(context, **response_kwargs)

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipes/recipe/recipe_detail.html"
    context_object_name = "recipe"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("user")
            .prefetch_related(
                "recipecategory_set__category",
                "recipeingredient_set__ingredient",
            )
        )

class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeUpdateForm
    template_name = "recipes/actions/recipe_updating.html"

    def get_queryset(self):
        return Recipe.objects.filter(user=self.request.user)\

    def get_success_url(self):
        return reverse("recipe_detail", kwargs={"pk": self.object.pk})

class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = "recipes/actions/delete_confirmation.html"
    success_url = reverse_lazy("recipe_list")

    def get_queryset(self):
        return Recipe.objects.filter(user=self.request.user)

class UserRecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "recipes/user_recipes.html"
    context_object_name = "recipes"

    def get_queryset(self):
        return (super()
              .get_queryset()
              .select_related("user")
              .filter(user=self.request.user))


class RecipeIngredientSearchView(FormView):
    template_name = "recipes/home/main_block.html"
    form_class = IngredientSearchForm

    def form_valid(self, form):
        ingredients = form.cleaned_data["ingredients"]
        cleaned_ingredients = ",".join(i.strip() for i in ingredients.split(",") if i.strip())
        api_data = get_recipes_by_ingredients(cleaned_ingredients)
        context = self.get_context_data(form=form, ingredients=cleaned_ingredients, recipes=api_data)
        return self.render_to_response(context)

