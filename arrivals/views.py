from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import datetime


# API pogled za registracijo prihoda z uporabo kartice
@api_view(['POST'])
def arrival_by_card(request):
    card_id = request.data.get('card_id')
    date_time_str = request.data.get('date_time')
    # Preveri zahtevane podatke
    if not card_id or not date_time_str:
        return Response({"error": "card_id and date_time are required."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        # Poskusi pretvoriti datum in čas
        dt = datetime.datetime.strptime(date_time_str, "%d.%m.%Y %H:%M:%S")
    except ValueError:
        try:
            dt = datetime.datetime.strptime(date_time_str, "%d.%m.%Y %H:%M")
        except ValueError:
            return Response({"error": "date_time must be in format DD.MM.YYYY HH:MM[:SS]"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        # Poišče udeleženca po številki kartice
        attendee = Attendee.objects.get(card_number=card_id)
    except Attendee.DoesNotExist:
        return Response({"error": "Attendee with this card_id does not exist."}, status=status.HTTP_404_NOT_FOUND)
    # Ustvari prihod
    Arrival.objects.create(attendee=attendee, arrived_at=dt)
    return Response({"status": "ok"})

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Arrival, Attendee
from rest_framework.decorators import api_view
from rest_framework.response import Response
from attendees.models import Attendee



# Pogled za prikaz seznama prihodov
def arrival_list(request):
    arrivals = Arrival.objects.all()
    attendees = Attendee.objects.all()

    # Filtriranje po datumu, če je podan
    if request.GET.get('date'):
        arrivals = arrivals.filter(arrived_at__date=request.GET['date'])

    if request.GET.get('attendee'):
        arrivals = arrivals.filter(attendee_id=request.GET['attendee'])

    return render(request, 'arrivals/list.html', {'arrivals': arrivals, 'attendees': attendees})




