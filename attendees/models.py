from django.db import models
from django.contrib import admin
from django.contrib.auth import get_user_model


# Model za udeleženca
class Attendee(models.Model):
    first_name = models.CharField(max_length=100)  # Ime
    last_name = models.CharField(max_length=100)   # Priimek
    birth_date = models.DateField()                # Datum rojstva
    card_number = models.CharField(max_length=50, unique=True)  # Številka kartice

    created_at = models.DateTimeField(auto_now_add=True)        # Datum vnosa

    def __str__(self):
        # Prikaz udeleženca kot ime in priimek
        return f"{self.first_name} {self.last_name}"
    

# Model za beleženje sprememb posameznih polj udeleženca
class AttendeeChangeLog(models.Model):
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)  # Povezava na udeleženca
    field = models.CharField(max_length=100)                          # Spremenjeno polje
    old_value = models.CharField(max_length=255, null=True, blank=True) # Stara vrednost
    new_value = models.CharField(max_length=255)                      # Nova vrednost
    changed_at = models.DateTimeField(auto_now_add=True)              # Datum spremembe


# Model za beleženje večjih sprememb udeleženca
class AttendeeChange(models.Model):
    ACTION_CHOICES = [
        ('add', 'Dodaj'),
        ('edit', 'Uredi'),
        ('delete', 'Delete'),
    ]
    attendee = models.ForeignKey('Attendee', on_delete=models.CASCADE, null=True, blank=True)  # Povezava na udeleženca
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)                           # Vrsta akcije
    timestamp = models.DateTimeField(auto_now_add=True)                                        # Čas spremembe
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True) # Uporabnik, ki je izvedel spremembo
    data_snapshot = models.JSONField()                                                         # Posnetek podatkov
    changed_fields = models.JSONField(null=True, blank=True, help_text="List of changed fields for edit actions.") # Seznam spremenjenih polj

    def __str__(self):
        # Prikaz spremembe
        return f'{self.get_action_display()} - {self.attendee} at {self.timestamp}'

# Admin vmesnik za AttendeeChangeLog
@admin.register(AttendeeChangeLog)
class AttendeeChangeLogAdmin(admin.ModelAdmin):
    search_fields = ['attendee__last_name', 'field']
    list_filter = ['changed_at']