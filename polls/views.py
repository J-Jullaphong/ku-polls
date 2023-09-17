from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Choice, Question, Vote
from logging import getLogger


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
        Handle GET request to display the details of a poll question.
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

                requested_user = request.user
                try:
                    previous_vote = Vote.objects.get(user=requested_user,
                                                     choice__question=question
                                                     ).choice.id
                except (Vote.DoesNotExist, TypeError):
                    previous_vote = 0
                return render(request, self.template_name,
                              {'question': question,
                               'previous_vote': previous_vote})
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


def get_client_ip(request):
    """Get the visitor’s IP address using request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@login_required
def vote(request, question_id):
    """
    vote() is responsible for handling user votes on a poll question.
    """
    question = get_object_or_404(Question, pk=question_id)
    requested_user = request.user
    ip_address = get_client_ip(request)
    logger = getLogger('polls')
    logger.info(f'{requested_user} logged in from {ip_address}')

    if not question.can_vote():
        messages.error(request, message=f"Poll {question_id} is not available "
                                        f"for voting.")
        return redirect('polls:index')

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        logger.warning(f'{requested_user} failed to vote {question} from {ip_address}')
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })

    try:
        # Find a vote for this user and this question
        vote = Vote.objects.get(user=requested_user, choice__question=question)
        # Update his vote
        vote.choice = selected_choice
    except Vote.DoesNotExist:
        # No matching vote - Create a new Vote
        vote = Vote(user=requested_user, choice=selected_choice)
    vote.save()
    logger.info(f'{requested_user} voted for {selected_choice} '
                f'in {question} from {ip_address}')
    messages.info(request, message=f"You voted for \"{selected_choice}\".")
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,
                                                               )))
