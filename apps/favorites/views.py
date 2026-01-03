from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from apps.favorites.models import UserFavorite
from apps.recipes.models import Recipe


@method_decorator(require_POST, name="dispatch")
class ToggleFavorite(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=pk)
        favourite, created = UserFavorite.objects.get_or_create(user=request.user, recipe=recipe)
        if not created:
            favourite.delete()

        return redirect(request.META.get('HTTP_REFERER', "home"))



class FavoritesView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'favorites/favorites.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        return (
            Recipe.objects
            .filter(favorited_by__user=self.request.user)
            .select_related("user")
            .distinct()
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["favorite_ids"] = set(
            self.request.user.favorites.values_list("recipe_id", flat=True)
        )
        return ctx