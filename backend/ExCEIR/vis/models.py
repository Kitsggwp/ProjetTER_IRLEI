"""
This module allows you to configure the database tables."""

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Team(models.Model):
    """
    Model for the team table
    """
    name = models.CharField(max_length=100, primary_key=True)
    """The name field is the primary key."""
    info = models.CharField(max_length=100, default="null")
    """The info field is used to add a description, it needs to be a string"""

    def __str__(self):
        return str(self.name)


class CustomUser(AbstractUser):
    """
    Model for the user table
    """
    team = models.CharField(max_length=100, default="null", null=True, blank=True)  # Utilise le champ 'name' comme clé étrangère
    """The team field specify the user's team, it can be null or blank for admin"""
    info = models.CharField(max_length=100, default="null", null=True, blank=True)
    """The info field is used to add a description, it needs to be a string"""
    def __str__(self):
        return self.username


class Eval(models.Model):
    """
    Model for the eval table
    """
    System_id = models.CharField(max_length=100, default="null")
    """The system_id field is a character field for the system name"""
    System_collection = models.CharField(max_length=100, default="null", null=True, blank=True)
    """The System_collection is optionnal"""
    Round = models.CharField(max_length=100, default="null")
    """The round field corresponds to the system round"""
    Query = models.CharField(max_length=100, default="null")
    """The query field corresponds to the query line in the eval file"""
    Metric = models.CharField(max_length=100, default="null")
    """The metric field corresponds to the metric line in the eval file"""
    Value = models.CharField(max_length=100, default="null")
    """The value field corresponds to the value line in the eval file"""
    Team = models.ForeignKey(Team, on_delete=models.CASCADE, to_field='name')  # Utilise le champ 'name' comme clé étrangère
    """The team field is a foreign key to specify the system's team"""
    class Meta:
        """
            Meta options for the Eval model.
        """
        unique_together = (('System_id', 'Round', 'Query', 'Metric'),)
        """Fields 'System_id', 'Round', 'Query', 'Metric' must be unique"""

        indexes = [
            models.Index(fields=['Round']),
            models.Index(fields=['Query']),
            models.Index(fields=['Metric']),
            models.Index(fields=['System_id']),
        ]
        """Index definitions for the Eval model"""

    def __str__(self):
        return str(self.System_id)


