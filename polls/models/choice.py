from django.db import models

from .question import Question


class Choice(models.Model):
    """
    Choice Model represents a choice in a question with its text
    and votes count.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    @property
    def votes(self):
        """Count the votes for this choice."""
        return self.vote_set.count()

    def __str__(self):
        """
        Returns a string that represents the text of the choice.
        """
        return self.choice_text
