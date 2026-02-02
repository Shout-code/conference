from django.db import models
from attendees.models import Attendee


# Model za prihod udeleženca
class Arrival(models.Model):
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)  # Povezava na udeleženca
    arrived_at = models.DateTimeField()                               # Datum in čas prihoda

    def __str__(self):
        # Prikaz prihoda v obliki: udeleženec - datum
        return f"{self.attendee} - {self.arrived_at}"