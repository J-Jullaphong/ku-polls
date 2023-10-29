from django.contrib.auth.models import User
from django.db import models

from .choice import Choice


class Vote(models.Model):
    """Vote model records a Vote of a Choice by a User."""
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
