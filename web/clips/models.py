from django.db import models


class Clip(models.Model):
    timestamp = models.DateTimeField()
    duration = models.DurationField()
    file_name = models.CharField(max_length=200)
    anomaly = models.FloatField(default=0)
