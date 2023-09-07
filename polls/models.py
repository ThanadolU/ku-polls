import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    """Model for Question with publish date."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.localtime()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    def __str__(self):
        return self.question_text
    
    def is_published(self):
        now = timezone.localtime()
        return now >= self.pub_date

    def can_vote(self):
        now = timezone.localtime()
        if self.end_date is None:
            return now >= self.pub_date
        return self.pub_date <= now <= self.end_date


class Choice(models.Model):
    """Model for Choice that has relevant with Question"""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
