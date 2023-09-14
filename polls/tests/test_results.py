from django.test import TestCase
from django.urls import reverse

from .base import create_question


class QuestionResultsViewTests(TestCase):

    def test_future_question_results_page(self):
        """
        The results for unpublished questions should not be accessible.
        """
        question = create_question(question_text='Test.', days=20)
        url = reverse('polls:results', args=(question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
