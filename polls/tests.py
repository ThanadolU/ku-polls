import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


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
        current_question = Question(pub_date=time, end_date=time+datetime.timedelta(seconds=1))
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


class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """
        If no questions exist, an appropriate messsage is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on
        the index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't dislayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [],
        )

    def test_future_question_and_past_question(self):
        """
        Even if both past and future exists, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The question index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 302 redirect back to the detail page.
        """
        future_question = create_question(question_text='Future question.',
                                          days=10)
        url = reverse('polls:detail', args=(future_question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past question.',
                                        days=-5)
        url = reverse('polls:detail', args=(past_question.id, ))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionResultsViewTests(TestCase):

    def test_correct_vote_count_display(self):
        """
        The result view of question that show the right
        vote count for each choice.
        """
        question = create_question(question_text='Test.', days=-2)
        create_choice(question=question, choice_text="choice 1")
        choice = question.choice_set.get(pk=1)
        choice.votes += 1
        choice.save()
        url = reverse('polls:results', args=(question.id,))
        response = self.client.get(url)
        self.assertContains(
            response,
            f'{choice.choice_text} -- {choice.votes}'
        )

    def test_future_question_results_page(self):
        """
        The results for unpublished questions should not be accessible.
        """
        question = create_question(question_text='Test.', days=20)
        url = reverse('polls:results', args=(question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
