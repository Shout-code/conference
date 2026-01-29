from django.contrib import admin
from django.urls import path

from .views import auth_view, attendee_add, attendee_list, arrival_add, arrival_list, attendee_edit, login_view, register_view, attendee_change_list
from attendees.views import attendees_api
from arrivals.views import arrival_by_card_api
from arrivals.views import arrival_by_card_api, arrival_by_card_now_api


urlpatterns = [
    path('', auth_view, name='auth'),  
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('admin/', admin.site.urls),
    path('attendees/add/', attendee_add, name='attendee_add'),
    path('attendees/list/', attendee_list, name='attendee_list'),
    path('arrivals/add/', arrival_add, name='arrival_add'),
    path('arrivals/list/', arrival_list, name='arrival_list'),
    path('attendees/edit/<int:pk>/', attendee_edit, name='attendee_edit'),
    path('attendee-changes/', attendee_change_list, name='attendee_change_list'),
    path('api/attendees/', attendees_api, name='attendees_api'),
    path('api/arrivals/by-card/', arrival_by_card_api, name='arrival_by_card_api'),
    path('api/arrivals/by-card-now/', arrival_by_card_now_api, name='arrival_by_card_now_api'),
]



