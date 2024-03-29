"""This module contains Question model."""
import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    """Model for Question with publish date."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField(null=True, blank=True)

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        """Return boolean whether it was published recently."""
        now = timezone.localtime()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        """Return readable string of each question."""
        return self.question_text

    def is_published(self):
        """Return boolean when the question was published."""
        now = timezone.localtime()
        return now >= self.pub_date

    def can_vote(self):
        """Return boolean when voting is allowed."""
        now = timezone.localtime()
        if self.end_date is None:
            return now >= self.pub_date
        return self.pub_date <= now <= self.end_date
