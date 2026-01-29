from django.contrib import admin
from .models import AttendeeChange

@admin.register(AttendeeChange)
class AttendeeChangeAdmin(admin.ModelAdmin):
    list_display = ('attendee', 'action', 'timestamp', 'user')
    search_fields = ('attendee__first_name', 'attendee__last_name', 'user__username', 'action')
    list_filter = ('action', 'timestamp', 'user')