from django.db import models
from django.contrib.auth.models import User

class StationPrefs(models.Model):
    owner = models.ForeignKey(User)
    station = models.TextField(max_length=300)

    def __str__(self):
        """Return string representation of the model"""
        return self.station
