from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .constants import LIST_PER_PAGE

User = get_user_model()

admin.site.register(User, UserAdmin)


class UserAdmin(admin.ModelAdmin):
    """Custom UserAdmin class"""

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
    )
    list_filter = ('username', 'email', 'role')
    search_fields = ('username', 'email', 'role')
    list_editable = ('role',)
    list_per_page = LIST_PER_PAGE
