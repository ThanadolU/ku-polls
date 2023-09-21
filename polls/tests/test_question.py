import datetime

from django.test import TestCase
from django.utils import timezone

from polls.models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.localtime() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.localtime() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.localtime() - datetime.timedelta(
                                        hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_for_question_in_the_future_pub_date(self):
        """
        is_published() return False means that you cannot vote.
        """
        time = timezone.localtime() + datetime.timedelta(days=10)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_published(), False)

    def test_is_published_for_question_in_the_default_pub_date(self):
        """
        is_published() return True means that you can vote.
        """
        current_question = Question(pub_date=timezone.localtime())
        self.assertIs(current_question.is_published(), True)

    def test_is_published_for_question_in_the_past_pub_date(self):
        """
        is_published() return True means that you can vote.
        """
        time = timezone.localtime() - datetime.timedelta(days=10)
        past_question = Question(pub_date=time)
        self.assertIs(past_question.is_published(), True)

    def test_can_vote_for_question_in_future(self):
        """
        can_vote() returns False (voting is not allowed)
        because it is not pub_date.
        """
        time = timezone.localtime() + datetime.timedelta(days=20)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.can_vote(), False)

    def test_can_vote_for_question_in_current(self):
        """
        can_vote() return True (voting is allowed) because pub_date
        and end_date are in the same date but different seconds.
        """
        time = timezone.localtime()
        current_question = Question(pub_date=time,
                                    end_date=time+datetime
                                    .timedelta(seconds=1))
        self.assertIs(current_question.can_vote(), True)

    def test_can_vote_for_question_in_past(self):
        """
        can_vote() return False (voting is allowed) because
        current time is after end_date.
        """
        time = timezone.localtime() - datetime.timedelta(days=-10)
        past_question = Question(pub_date=time, end_date=timezone.localtime())
        self.assertIs(past_question.can_vote(), False)

    def test_can_vote_with_no_end_date(self):
        """
        can_vote() return True (voting is allowed) for no end_date.
        """
        question = Question(pub_date=timezone.localtime())
        self.assertIs(question.can_vote(), True)
