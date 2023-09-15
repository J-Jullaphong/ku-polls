import datetime

from django.test import TestCase
from django.utils import timezone

from polls.models import Question


def create_question(question_text, days=0, duration=0):
    """
    Create a question with the given 'question_text' and published the given
    number of 'days' offset to now (negative for questions published in the
    past, positive for questions that have yet to be published) and make it
    available for a duration (if any) after publishing.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    if not duration:
        return Question.objects.create(question_text=question_text,
                                       pub_date=time)
    end_time = time + datetime.timedelta(days=duration)
    return Question.objects.create(question_text=question_text, pub_date=time,
                                   end_date=end_time)


class QuestionModelVotingTests(TestCase):
    def test_can_vote_with_published_question(self):
        """
        can_vote() returns True for questions that are available for voting.
        """
        question = create_question(question_text='Published question.',
                                   days=-5, duration=10)
        self.assertTrue(question.can_vote())

    def test_can_vote_with_recent_question(self):
        """
        can_vote() returns True for questions that are recently
        available for voting.
        """
        question = create_question(question_text='Published question.',
                                   duration=3)
        self.assertTrue(question.can_vote())

    def test_can_vote_no_end_date_question(self):
        """
        can_vote() returns True for questions that have no end date.
        """
        question = create_question(question_text='Published question.')
        self.assertTrue(question.can_vote())

    def test_cannot_vote_before_pub_date(self):
        """
        can_vote() returns False for questions that are not yet
        available for voting.
        """
        question = create_question(question_text='Future question.', days=30)
        self.assertFalse(question.can_vote())

    def test_cannot_vote_after_end_date(self):
        """
        can_vote() returns False for questions that have ended voting.
        """
        question = create_question(question_text='Ended question.',
                                   days=-5, duration=3)
        self.assertFalse(question.can_vote())
