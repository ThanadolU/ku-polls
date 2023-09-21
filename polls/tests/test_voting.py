from django.test import TestCase
from django.urls import reverse

from polls.models import Vote
from django.contrib.auth.models import User

from .base import create_question, create_choice


class VoteModelTests(TestCase):

    def setUp(self):
        """Set up the user before running test."""
        self.credentials = {
            'username': 'test_user',
            'password': 'secret'
        }
        self.user = User.objects.create_user(**self.credentials)
        self.user.save()

    def test_authenticated_user_can_vote(self):
        """Authenticated user can vote."""
        self.client.login(username='test_user', password='secret')
        question = create_question(question_text='test', days=1)
        response = self.client.post(reverse('polls:vote',
                                            args=(question.id, )))
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_user_cannot_vote(self):
        """Unauthenticated user cannot vote."""
        question = create_question(question_text='test', days=1)
        response = self.client.post(reverse('polls:vote',
                                            args=(question.id, )))
        self.assertEqual(response.status_code, 302)

    def test_one_user_one_vote(self):
        """One user can vote once per question."""
        self.client.login(username='test_user', password='secret')
        question = create_question(question_text='test', days=1)
        choice1 = create_choice(question=question, choice_text='choice 1')
        choice2 = create_choice(question=question, choice_text='choice 2')
        response = self.client.post(reverse('polls:vote',
                                    args=(question.id, )),
                                    {'choice': choice1.id})
        self.assertEqual(Vote.objects.get(
            user=self.user,
            choice__question=question).choice, choice1
        )
        self.assertEqual(Vote.objects.all().count(), 1)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(
            reverse('polls:vote', args=(question.id,)),
            {'choice': choice2.id}
        )
        self.assertEqual(Vote.objects.get(
            user=self.user,
            choice__question=question).choice, choice2
        )
        self.assertEqual(Vote.objects.all().count(), 1)
        self.assertEqual(response.status_code, 302)
