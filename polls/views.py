from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set 
        to be published in the future).
        """
        # return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(pub_date__lte=timezone.localtime()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.localtime())
    
    def get(self, request, pk):
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist as e:
            raise Http404('Question does not exist') from e
        if not question.is_published():
            messages.error(request, 'This question is not published')
            return HttpResponseRedirect(reverse('polls:index'))
        if not question.can_vote():
            messages.error(request, 'You cannot vote unpublished or ended question')
            return HttpResponseRedirect(reverse('polls:index'))
        return render(request, 'polls/detail.html', {'question': question})


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.localtime())
    
    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        if not question.is_published():
            messages.error(request, 'You cannot watch the result of unpublished or ended question')
            return HttpResponseRedirect(reverse('polls:index'))
        return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        messages.error(request, "You didn't select a choice!")
        return render(request, 'polls/detail.html', {
            'question': question,
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
