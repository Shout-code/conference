from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    # Obrazec za registracijo uporabnika
    first_name = forms.CharField(max_length=100)  # Ime
    last_name = forms.CharField(max_length=100)   # Priimek
    email = forms.EmailField()                    # E-pošta
    
    class Meta(UserCreationForm.Meta):
        # Nastavitve za model in polja
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')