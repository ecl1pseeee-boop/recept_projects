from datetime import timedelta

from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, TemplateView, CreateView
from django.db.models import Q
from .forms import RecipeForm, RecipeFilterForm
from .models import Recipe, Category, RecipeCategory


class HomeView(TemplateView):
    template_name = "recipes/index.html"

class RecipeListView(ListView):
    model = Recipe
    context_object_name = "recipes"
    template_name = "recipes/recipe_list.html"
    partial_template_name = "recipes/recipes_page.html"

    def get_filter_form(self) -> RecipeFilterForm:
        return RecipeFilterForm(self.request.GET)


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
            qs = qs.filter(image_url__isnull=False).exclude(image_url="")

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


class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "recipes/recipe_create.html"
    success_url = reverse_lazy("recipe_list")

