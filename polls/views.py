"""This module contains the views of each page of the application."""
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Vote
# from django.contrib.auth.forms import UserCreationForm

from .models import Question, Choice


class IndexView(generic.ListView):
    """Index page of application."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set
        to be published in the future).
        """
        # return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(pub_date__lte=timezone.localtime())\
            .order_by('-pub_date')


class DetailView(generic.DetailView):
    """Detail page of application."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.localtime())

    def get(self, request, pk):
        """Return different pages depend on is_published and can_vote.
        Return index page if is_published or can_vote are true.
        If not return detail page.
        """
        user = request.user
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            messages.error(request, 'Question does not exist')
            # redirect back to index page
            return redirect('/')
        if not question.is_published():
            messages.error(request, 'This question is not published')
            return HttpResponseRedirect(reverse('polls:index'))
        if not question.can_vote():
            messages.error(request, 'You cannot vote unpublished \
                           or ended question')
            return HttpResponseRedirect(reverse('polls:index'))
        if not user.is_authenticated:
            return redirect('login')
        try:
            vote = Vote.objects.get(user=user, choice__question=question)
            selected_choice = vote.choice.choice_text
        except Vote.DoesNotExist:
            selected_choice = ''
        return render(request, 'polls/detail.html', {
                'question': question,
                'selected_choice': selected_choice
            })


class ResultsView(generic.DetailView):
    """Result page of application."""

    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.localtime())

    def get(self, request, pk):
        """Return different pages depend on is_published.
        Redirect index page if question does not exist or
        is_published is false. Return result page"""
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            messages.error(request, 'You cannot go to result \
                           page of the question does not exist')
            # redirect back to index page
            return redirect('/')
        if not question.is_published():
            messages.error(request, 'You cannot watch the result \
                           of unpublished or ended question')
            return HttpResponseRedirect(reverse('polls:index'))
        return render(request, 'polls/results.html', {'question': question})


@login_required(login_url="/accounts/login/")
def vote(request, question_id):
    """Add vote to selected choice of current question."""
    user = request.user
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        messages.error(request, "You didn't select a choice!")
        return render(request, 'polls/detail.html', {
            'question': question,
        })
    try:
        # find a vote for this user and this question
        vote = Vote.objects.get(user=user, choice__question=question)
        # update his/her vote
        vote.choice = selected_choice
    except Vote.DoesNotExist:
        # no matching vote - create a new Vote
        vote = Vote(user=user, choice=selected_choice)
    vote.save()
    messages.info(request, f'You\'re selected {selected_choice}')
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('polls:results',
                                        args=(question.id,)))
