import datetime

from django.contrib import admin
from django.db import models
from django.utils import timezone


class Question(models.Model):
    """
    Question Model represents a question with its text,
    publication and end dates.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    end_date = models.DateTimeField('date ended', default=None, null=True,
                                    blank=True)

    def __str__(self):
        """
        Returns a string that represents the text of the question.
        """
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        """
        Check if the question was published recently (within the last day).

        :return: True for questions that was published within the last day,
                 False otherwise.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """
        Check if the question is published.

        :return: True for questions that is published, False otherwise.
        """
        now = timezone.now()
        return self.pub_date <= now

    def can_vote(self):
        """
        Check if the question allows voting at a current time based on
        the publication date and end date (if any).

        :return: True for questions that allows voting at a current time,
                 False otherwise.
        """
        now = timezone.now()
        if self.end_date is not None:
            return self.pub_date <= now <= self.end_date
        return self.pub_date <= now
