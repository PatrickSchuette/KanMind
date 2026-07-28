from django.contrib import admin

from .models import Comment, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin configuration for the Task model."""

    list_display = ('title', 'board', 'status', 'priority','assignee', 'reviewer', 'due_date')
    list_filter = ('status', 'priority', 'board')
    search_fields = ('title', 'description')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin configuration for the Comment model."""

    list_display = ('task', 'author', 'created_at')
    list_filter = ('task__board',)
    search_fields = ('content', 'author__email')
