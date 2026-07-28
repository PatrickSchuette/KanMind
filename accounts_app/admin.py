from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin configuration for the UserProfile model."""

    list_display = ('fullname', 'user')
    search_fields = ('fullname', 'user__email')
