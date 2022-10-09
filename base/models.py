from django.db import models

# Create your models here.
class ResultSet(models.Model):
    weight = models.FloatField()
    total_credits = models.IntegerField()

