from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
# Prilagojen admin vmesnik za uporabnika
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Prikazana polja v seznamu
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    # Filtri za seznam
    list_filter = ('is_staff', 'is_active')
    # Iskalna polja
    search_fields = ('email', 'first_name', 'last_name')
    # Privzeto razvrščanje
    ordering = ('email',)
    # Skupine polj v obrazcu
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    # Skupine polj pri dodajanju
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )
