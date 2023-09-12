from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Choice, Question


class IndexView(generic.ListView):
    """
    IndexView displays a list of the 5 latest published questions.
    """
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()
                                       ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """
    DetailView displays the details of a poll question,
    including question text, and its choices.
    """
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """
        Handle GET request to display the details of of a poll question.
        If the question is allowed voting, render the detail page.
        If the question isn't allowed voting, redirect to the poll index page
        and display an error message.
        """
        try:
            question = get_object_or_404(Question, pk=kwargs['pk'])
        except Http404:
            messages.error(request, message=f"Poll {kwargs['pk']} not found.")
            return redirect('polls:index')
        else:
            if question.can_vote():
                return render(request, self.template_name,
                              {'question': question})
            else:
                messages.error(request,
                               message=f"Poll {kwargs['pk']} is not available "
                                       f"for voting.")
                return redirect('polls:index')


class ResultsView(generic.DetailView):
    """
    ResultsView displays the results of a poll question.
    """
    model = Question
    template_name = 'polls/results.html'

    def get(self, request, *args, **kwargs):
        """
        Handle GET request to display the results of a poll question.
        If the results are available, display the results.
        If the results are not available, redirect to the poll index page
        and display an error message.
        """
        try:
            question = get_object_or_404(Question, pk=kwargs['pk'])
        except Http404:
            messages.error(request, message=f"Poll {kwargs['pk']} not found.")
            return redirect('polls:index')
        else:
            if question.is_published():
                return render(request, self.template_name,
                              {'question': question})
            else:
                messages.error(request,
                               message=f"Poll {kwargs['pk']}'s result is not "
                                       f"available.")
                return redirect('polls:index')


@login_required
def vote(request, question_id):
    """
    vote() is responsible for handling user votes on a poll question.
    """
    question = get_object_or_404(Question, pk=question_id)

    if not question.can_vote():
        messages.error(request, message=f"Poll {question.id} is not available "
                                        f"for voting.")
        return redirect('polls:index')

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,
                                                                   )))
