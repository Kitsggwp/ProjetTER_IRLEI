from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class Query(models.Model):
    query_id = models.IntegerField(default=0)
    query_text = models.CharField(max_length=200)
    query_narrative = models.CharField(max_length=1000, blank=True)
    query_tc = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return str(self.query_id)


class Team(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return str(self.name)


class CustomUser(AbstractUser):
    team = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Eval(models.Model):
    System_id = models.CharField(max_length=100, default="null")
    System_collection = models.CharField(max_length=100, default="null")
    Round = models.CharField(max_length=100, default="null")
    Query = models.CharField(max_length=100, default="null")
    Metric = models.CharField(max_length=100, default="null")
    Value = models.CharField(max_length=100, default="null")
    Team = models.ForeignKey(Team, on_delete=models.CASCADE, to_field='name')  # Utilise le champ 'name' comme clé étrangère
    

    def __str__(self):
        return str(self.System_id)


