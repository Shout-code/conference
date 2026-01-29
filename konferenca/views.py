from django.contrib.auth import logout
# Log out view
def logout_view(request):
    logout(request)
    return redirect('auth')
from django.shortcuts import render, redirect
from attendees.models import Attendee, AttendeeChange
from arrivals.models import Arrival
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from attendees.forms import AttendeeForm
from django.contrib.admin.views.decorators import staff_member_required
import datetime
from django.db.models import Q

User = get_user_model()

def home(request):
    return render(request, 'base.html')

def attendee_add(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        birth_date_str = request.POST.get('birth_date')
        card_number = request.POST.get('card_number')
        birth_date = None
        try:
            # Accept both DD.MM.YYYY and YYYY-MM-DD for flexibility
            if birth_date_str and '.' in birth_date_str:
                birth_date = datetime.datetime.strptime(birth_date_str, "%d.%m.%Y").date()
            else:
                birth_date = datetime.datetime.strptime(birth_date_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            birth_date = None
            messages.error(request, "Datum rojstva ni veljaven. Uporabite obliko DD.MM.YYYY.")

        if card_number and Attendee.objects.filter(card_number=card_number).exists():
            messages.error(request, "Ta številka kartice je že uporabljena.")
        elif first_name and last_name and birth_date and card_number:
            attendee = Attendee.objects.create(
                first_name=first_name,
                last_name=last_name,
                birth_date=birth_date,
                card_number=card_number
            )
            from attendees.models import AttendeeChange
            from django.forms.models import model_to_dict
            AttendeeChange.objects.create(
                attendee=attendee,
                action='add',
                user=request.user if request.user.is_authenticated else None,
                data_snapshot=serialize_for_json(model_to_dict(attendee))
            )
            return redirect('attendee_list')
        elif not birth_date:
            messages.error(request, "Datum rojstva ni veljaven. Uporabite obliko DD.MM.LLLL.")
    return render(request, 'attendee_add.html')

def attendee_list(request):
    attendees = Attendee.objects.all()
    return render(request, 'attendee_list.html', {'attendees': attendees})

def arrival_add(request):
    attendees = Attendee.objects.all()
    if request.method == 'POST':
        attendee_id = request.POST.get('attendee_id')
        arrival_date = request.POST.get('arrival_date')
        arrival_time = request.POST.get('arrival_time')
        if attendee_id and arrival_date and arrival_time:
            attendee = Attendee.objects.get(id=attendee_id)
            if Arrival.objects.filter(attendee=attendee).exists():
                messages.error(request, "Ta udeleženec je že bil evidentiran s to številko kartice.")
            else:
                try:
                    arrived_at_str = f"{arrival_date} {arrival_time}"
                    arrived_at_dt = datetime.datetime.strptime(arrived_at_str, "%Y-%m-%d %H:%M")
                except ValueError:
                    arrived_at_dt = None
                if arrived_at_dt:
                    Arrival.objects.create(
                        attendee=attendee,
                        arrived_at=arrived_at_dt
                    )
                    return redirect('arrival_list')
                else:
                    messages.error(request, "Datum ali čas prihoda ni veljaven. Uporabite obliko YYYY-MM-DD in HH:MM.")
    return render(request, 'arrival_add.html', {'attendees': attendees})

def attendee_edit(request, pk):
    attendee = Attendee.objects.get(pk=pk)
    if request.method == 'POST':
        post_data = request.POST.copy()
        birth_date_str = post_data.get('birth_date')
        if birth_date_str:
            try:
                birth_date = datetime.datetime.strptime(birth_date_str, "%d.%m.%Y").date()
                post_data['birth_date'] = birth_date
            except ValueError:
                messages.error(request, "Datum rojstva ni veljaven. Uporabite obliko DD.MM.YYYY.")
        form = AttendeeForm(post_data, instance=attendee)
        if form.is_valid():
            changed_fields = []
            for field in form.changed_data:
                changed_fields.append(field)
            attendee = form.save()
            from attendees.models import AttendeeChange
            from django.forms.models import model_to_dict
            AttendeeChange.objects.create(
                attendee=attendee,
                action='edit',
                user=request.user if request.user.is_authenticated else None,
                data_snapshot=serialize_for_json(model_to_dict(attendee)),
                changed_fields=changed_fields if changed_fields else None
            )
            messages.success(request, "Udeleženec uspešno posodobljen.")
            return redirect('attendee_list')
        else:
            if 'birth_date' in form.errors:
                messages.error(request, "Datum rojstva ni veljaven.")
    else:
        form = AttendeeForm(instance=attendee)
    return render(request, 'attendee_edit.html', {'form': form, 'attendee': attendee})

def arrival_list(request):
    arrivals = Arrival.objects.select_related('attendee').all()
    attendees = Attendee.objects.all()

    date = request.GET.get('date')
    if date:
        arrivals = arrivals.filter(arrived_at__date=date)

    attendee_id = request.GET.get('attendee_id')
    if attendee_id:
        arrivals = arrivals.filter(attendee_id=attendee_id)

    return render(request, 'arrival_list.html', {'arrivals': arrivals, 'attendees': attendees})

def auth_view(request):
    return render(request, 'auth.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('attendee_add')
        else:
            messages.error(request, "Napačen email ali geslo.")
    return render(request, 'auth.html')

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not all([first_name, last_name, email, password1, password2]):
            messages.error(request, "Vsa polja so obvezna.")
        elif password1 != password2:
            messages.error(request, "Gesli se ne ujemata.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Uporabnik s tem emailom že obstaja.")
        else:
            user = User.objects.create_user(
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            messages.success(request, "Registracija uspešna! Prijavite se.")
            return redirect('auth')
    return render(request, 'auth.html')

@staff_member_required
def attendee_change_list(request):
    q = request.GET.get('q', '')
    changes = AttendeeChange.objects.all()
    if q:
        action_map = {
            'dodaj': 'add',
            'uredi': 'edit',
            'delete': 'delete',
        }
        q_lower = q.lower()
        action_value = action_map.get(q_lower)
        action_filter = Q()
        if action_value:
            action_filter = Q(action__iexact=action_value)
        changes = changes.filter(
            Q(attendee__first_name__icontains=q) |
            Q(attendee__last_name__icontains=q) |
            Q(user__email__icontains=q) |
            Q(action__icontains=q) |
            action_filter
        )
    changes = changes.order_by('-timestamp')

    formatted_changes = []
    for change in changes:
        ts = change.timestamp
        formatted_timestamp = ts.strftime('%d.%m.%Y %H:%M') if ts else ''

        birth_date = change.data_snapshot.get('birth_date')
        formatted_birth_date = ''
        if birth_date:
            try:
                from datetime import datetime
                formatted_birth_date = datetime.strptime(birth_date, '%Y-%m-%d').strftime('%d.%m.%Y')
            except Exception:
                formatted_birth_date = birth_date

        data_snapshot = dict(change.data_snapshot)
        data_snapshot['birth_date'] = formatted_birth_date

        formatted_changes.append({
            'attendee': change.attendee,
            'get_action_display': change.get_action_display(),
            'user': change.user,
            'timestamp': formatted_timestamp,
            'data_snapshot': data_snapshot,
            'changed_fields': change.changed_fields if hasattr(change, 'changed_fields') else None,
        })

    return render(request, 'attendee_change_list.html', {'changes': formatted_changes})

def serialize_for_json(data):
    for k, v in data.items():
        if isinstance(v, (datetime.date, datetime.datetime)):
            data[k] = v.isoformat()
    return data