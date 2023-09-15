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


class QuestionModelDateTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59,
                                                   seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_future_question(self):
        """
        is_published() returns False for questions whose pub_date is
        in the future.
        """
        question = create_question(question_text='Future question.', days=30)
        self.assertFalse(question.is_published())

    def test_is_published_with_recent_question(self):
        """
        is_published() returns True for questions whose pub_date is
        recently.
        """
        question = create_question(question_text='Recent question.')
        self.assertTrue(question.is_published())

    def test_is_published_with_old_question(self):
        """
        is_published() returns True for questions whose pub_date is
        already passed.
        """
        question = create_question(question_text='Old question.', days=-1)
        self.assertTrue(question.is_published())
