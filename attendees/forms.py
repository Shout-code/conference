from django import forms
from .models import Attendee


# Obrazec za vnos udeleženca
class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = ['first_name', 'last_name', 'birth_date', 'card_number']
