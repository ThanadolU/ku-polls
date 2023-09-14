"""This module is base module."""

import datetime

from django.utils import timezone

from polls.models import Question


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.localtime() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


def create_choice(question: Question, choice_text):
    """
    Create a new choice for specific question.
    """
    return question.choice_set.create(choice_text=choice_text)
