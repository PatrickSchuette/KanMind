from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """Extends the built-in User model with a full name field."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    fullname = models.CharField(max_length=100)

    class Meta:
        ordering = ['fullname']
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        """Return a readable string representation of the profile."""
        return self.fullname
