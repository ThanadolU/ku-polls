from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User

from .base import create_question


class QuestionDetailViewTests(TestCase):

    def setUp(self):
        """Set up the user before running test."""
        self.credentials = {
            'username': 'test_user',
            'password': 'secret'
        }
        self.user = User.objects.create_user(**self.credentials)
        self.user.save()

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
        self.client.login(username='test_user', password='secret')
        past_question = create_question(question_text='Past question.',
                                        days=-5)
        url = reverse('polls:detail', args=(past_question.id, ))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
