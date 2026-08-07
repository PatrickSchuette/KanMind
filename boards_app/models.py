from django.contrib.auth.models import User
from django.db import models


class Board(models.Model):
    """Represents a kanban board owned by a user with multiple members."""

    title = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_boards')
    members = models.ManyToManyField(User, blank=True, related_name='member_boards')

    class Meta:
        ordering = ['title']
        verbose_name = 'Board'
        verbose_name_plural = 'Boards'

    def __str__(self):
        """Return a readable string representation of the board."""
        
        return f"{self.title} (Owner: {self.owner})"
