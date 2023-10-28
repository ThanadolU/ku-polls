"""This module contains Vote model."""
from django.db import models
from django.contrib.auth.models import User
from .choice import Choice


class Vote(models.Model):
    """Record a Vote of a Choice by a User."""
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def question(self):
        """Question of that choice"""
        return self.choice.question
