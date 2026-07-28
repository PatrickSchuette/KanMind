from django.contrib import admin

from .models import Board


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    """Admin configuration for the Board model."""

    list_display = ('title', 'owner', 'member_count')
    search_fields = ('title', 'owner__email')
    filter_horizontal = ('members',)

    def member_count(self, obj):
        """Return the number of members on this board."""
        return obj.members.count()
