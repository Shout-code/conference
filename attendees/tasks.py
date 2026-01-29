from django.utils import timezone
from .models import Attendee
from django.conf import settings
from django.core.mail import send_mail

from celery import shared_task

@shared_task
def daily_new_attendees_report():
    today = timezone.now().date()
    attendees = Attendee.objects.filter(created_at__date=today)
    attendee_lines = [
        f"{a.first_name} {a.last_name} ({a.card_number}) - {a.birth_date}"
        for a in attendees
    ]
    attendee_list = "\n".join(attendee_lines) if attendee_lines else "Ni novih udeležencev danes."
    message = f"Danes dodani: {attendees.count()}\n\n{attendee_list}"
    send_mail(
        subject="Dnevni novi udeleženci",
        message=message,
        recipient_list=["admin@example.com"],
        from_email="noreply@conference.com"
    )