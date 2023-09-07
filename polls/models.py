import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    """Model for Question with publish date."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=False)
    end_date = models.DateTimeField(null=True, blank=True)

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    def is_published(self):
        return timezone.now() > self.pub_date

    def can_vote(self):
        if self.end_date is not None:
            return self.pub_date < timezone.now() < self.end_date
        return True

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    """Model for Choice that has relevant with Question"""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
