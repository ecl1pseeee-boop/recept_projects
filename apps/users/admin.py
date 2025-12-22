from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Дополнительная информация'
    fields = ('avatar', )

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="100" height="100" style="border-radius: 50%;" />', obj.avatar.url)
        return "No avatar"
    avatar_preview.short_description = 'Превью аватара'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_per_page = 10
    list_max_show_all = 100
    list_select_related = ('user',)
    autocomplete_fields = ('user',)
    raw_id_fields = ('user',)