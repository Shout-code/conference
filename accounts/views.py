from django.shortcuts import render

# Pogledi za aplikacijo accounts
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignUpForm # type: ignore

# Pogled za registracijo novega uporabnika
class SignUpView(CreateView):
    # Uporablja obrazec za registracijo
    form_class = SignUpForm
    # Preusmeritev po uspešni registraciji
    success_url = reverse_lazy('login')
    # Predloga za prikaz registracije
    template_name = 'accounts/signup.html'