from django.shortcuts import render


from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignUpForm # type: ignore

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'