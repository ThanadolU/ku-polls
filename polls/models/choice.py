"""This module contains Choice model."""
from django.db import models
from .question import Question


class Choice(models.Model):
    """Model for Choice that has relevant with Question"""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    # votes = models.IntegerField(default=0)

    @property
    def votes(self):
        """Count the votes for this choice"""
        # count = Vote.objects.filter(choice=self).count()
        return self.vote_set.count()

    def __str__(self):
        """Return readable string of each choice."""
        return self.choice_text
