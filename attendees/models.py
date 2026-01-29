from django.db import models
from django.contrib import admin
from django.contrib.auth import get_user_model

class Attendee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    card_number = models.CharField(max_length=50, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    


class AttendeeChangeLog(models.Model):
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    field = models.CharField(max_length=100)
    old_value = models.CharField(max_length=255, null=True, blank=True)
    new_value = models.CharField(max_length=255)
    changed_at = models.DateTimeField(auto_now_add=True)



class AttendeeChange(models.Model):
    ACTION_CHOICES = [
        ('add', 'Dodaj'),
        ('edit', 'Uredi'),
        ('delete', 'Delete'),
    ]
    attendee = models.ForeignKey('Attendee', on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    data_snapshot = models.JSONField()
    changed_fields = models.JSONField(null=True, blank=True, help_text="List of changed fields for edit actions.")

    def __str__(self):
        return f'{self.get_action_display()} - {self.attendee} at {self.timestamp}'

@admin.register(AttendeeChangeLog)
class AttendeeChangeLogAdmin(admin.ModelAdmin):
    search_fields = ['attendee__last_name', 'field']
    list_filter = ['changed_at']