from django.contrib import admin
from django.urls import path

from .views import auth_view, attendee_add, attendee_list, arrival_add, arrival_list, attendee_edit, login_view, register_view, attendee_change_list, logout_view
from attendees.views import attendees_api
from arrivals.views import arrival_by_card


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
    path('api/arrival_by_card/', arrival_by_card, name='arrival_by_card'),
    path('logout/', logout_view, name='logout'),
]



