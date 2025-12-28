from django.contrib import admin
from django.contrib.auth.models import User

from .models import Ingredient, UserIngredient

admin.site.register(Ingredient)
admin.site.register(UserIngredient)

