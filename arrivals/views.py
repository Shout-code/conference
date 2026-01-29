from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Arrival, Attendee
from .serializers import ArrivalCreateSerializer
from .serializers import ArrivalCreateSerializer, ArrivalByCardNowSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from attendees.models import Attendee


def arrival_list(request):
    arrivals = Arrival.objects.all()
    attendees = Attendee.objects.all()

    if request.GET.get('date'):
        arrivals = arrivals.filter(arrived_at__date=request.GET['date'])

    if request.GET.get('attendee'):
        arrivals = arrivals.filter(attendee_id=request.GET['attendee'])

    return render(request, 'arrivals/list.html', {'arrivals': arrivals, 'attendees': attendees})



@api_view(['POST'])
def arrival_by_card_api(request):
    serializer = ArrivalCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    attendee = get_object_or_404(Attendee, card_number=serializer.validated_data['card_number'])
    Arrival.objects.create(
        attendee=attendee,
        arrived_at=serializer.validated_data['arrived_at']
    )
    return Response({"status": "ok"})



from django.utils import timezone
from rest_framework import status

@api_view(['POST'])
def arrival_by_card_now_api(request):
    serializer = ArrivalByCardNowSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    attendee = get_object_or_404(Attendee, card_number=serializer.validated_data['card_number'])
    if Arrival.objects.filter(attendee=attendee).exists():
        return Response({"error": "Ta udeleženec je že bil evidentiran s to številko kartice."}, status=status.HTTP_400_BAD_REQUEST)
    Arrival.objects.create(
        attendee=attendee,
        arrived_at=timezone.now()
    )
    return Response({"status": "ok"})

