from django.db import models
from attendees.models import Attendee

class Arrival(models.Model):
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    arrived_at = models.DateTimeField()

    def __str__(self):
        return f"{self.attendee} - {self.arrived_at}"