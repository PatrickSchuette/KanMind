from django.contrib.auth.models import User
from django.db import models

from boards_app.models import Board

class Task(models.Model):
    """Represents a task on a board with status, priority, assignee, and reviewer."""

    class Status(models.TextChoices):
        TODO = 'to-do', 'To Do'
        IN_PROGRESS = 'in-progress', 'In Progress'
        REVIEW = 'review', 'Review'
        DONE = 'done', 'Done'

    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_tasks', null=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=300)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TODO)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.LOW)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_tasks')
    due_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['due_date']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        """Return a readable string representation of the task."""
        
        return f"{self.title} ({self.get_status_display()})"


class Comment(models.Model):
    """A user comment attached to a task."""

    created_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_comments')
    content = models.TextField(max_length=300)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        """Return a readable string representation of the comment."""
        
        return f"Comment by {self.author} on {self.task}"
