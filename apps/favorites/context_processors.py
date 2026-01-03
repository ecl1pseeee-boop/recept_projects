def favorite_ids(request):
    if request.user.is_authenticated:
        return {
            "favorite_ids" : set(request.user.favorites.values_list("recipe_id", flat=True))
        }
    return {
        "favorite_ids" : set()
    }