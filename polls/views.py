"""This module contains the views of each page of the application."""
from django.http import HttpResponseRedirect, Http404
from django.utils import timezone
from django.urls import reverse
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Choice, Vote
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(generic.ListView):
    """Index page of application."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions
        (not including those set to be published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.localtime()).order_by('-pub_date')[:5]


class DetailView(LoginRequiredMixin, generic.DetailView):
    """Detail page of application."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.localtime())

    def get(self, request, pk):
        """Return different pages depend on is_published and can_vote.
        Return index page if is_published or can_vote are true.
        If not return detail page.
        """
        user = request.user
        try:
            question = get_object_or_404(Question, pk=pk)
        except Http404:
            messages.error(request, 'We don\'t have this question')
            return HttpResponseRedirect(reverse('polls:index'))
        if not question.is_published():
            messages.error(request, 'This poll is not published.')
            return HttpResponseRedirect(reverse('polls:index'))
        if not question.can_vote():
            messages.error(request, 'Voting period has ended.')
            return HttpResponseRedirect(reverse('polls:index'))
        if not user.is_authenticated:
            return redirect('login')
        try:
            vote_object = Vote.objects.get(user=user,
                                           choice__in=question.choice_set.all())
            selected_choice = vote_object.choice.choice_text
        except Vote.DoesNotExist:
            selected_choice = ''
        return render(request, 'polls/detail.html', {'question': question,
                                                     'selected_choice': selected_choice})


class ResultsView(generic.DetailView):
    """Result page of application."""

    model = Question
    template_name = 'polls/results.html'

    def get(self, request, pk):
        """Return result page if is_published method returns true.
        If not redirect to the index page.
        """
        question = get_object_or_404(Question, pk=pk)
        if question.is_published():
            return render(request,
                          'polls/results.html',
                          {'question': question, })
        messages.error(request, 'This poll is not available.')
        return HttpResponseRedirect(reverse('polls:index'))


@login_required
def vote(request, question_id):
    """Add vote to selected choice of current question."""
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        try:
            vote_object = Vote.objects.get(user=user,
                                           choice__in=question.choice_set.all())
            vote_object.choice = selected_choice
            vote_object.save()
        except Vote.DoesNotExist:
            Vote.objects.create(user=user, choice=selected_choice).save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
