from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ResultSet(models.Model):
    weight = models.FloatField()
    total_credits = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

