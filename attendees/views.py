from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AttendeeSerializer
from .models import Attendee
from .forms import AttendeeForm  # type: ignore
from django.contrib import messages
from datetime import datetime

def attendee_list(request):
    attendees = Attendee.objects.all()
    return render(request, 'attendee_list.html', {'attendees': attendees})

from django.contrib import messages
from datetime import datetime

def attendee_add(request):
    if request.method == 'POST':
        form = AttendeeForm(request.POST)
        if form.is_valid():
            try:
                birth_date = form.cleaned_data['birth_date']
                form.save()
                messages.success(request, "Udeleženec uspešno dodan.")
                return redirect('attendee_list')
            except ValueError:
                messages.error(request, "Datum rojstva ni veljaven.")
        else:
            if 'birth_date' in form.errors:
                messages.error(request, "Datum rojstva ni veljaven.")
    else:
        form = AttendeeForm()
    return render(request, 'attendee_form.html', {'form': form})


@api_view(['GET'])
def attendees_api(request):
    return Response(AttendeeSerializer(Attendee.objects.all(), many=True).data)