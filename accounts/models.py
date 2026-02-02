from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    # Upravljalec uporabnikov po meri
    def create_user(self, email, password=None, **extra_fields):
        # Ustvari navadnega uporabnika
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Ustvari superuporabnika
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# Model uporabnika po meri
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # E-pošta kot uporabniško ime
    first_name = models.CharField(max_length=30, blank=True)  # Ime
    last_name = models.CharField(max_length=30, blank=True)   # Priimek
    is_active = models.BooleanField(default=True)             # Aktivnost
    is_staff = models.BooleanField(default=False)             # Pravice osebja

    objects = CustomUserManager()  # Upravljalec

    USERNAME_FIELD = 'email'       # Polje za prijavo
    REQUIRED_FIELDS = []

    def __str__(self):
        # Prikaz uporabnika kot e-pošta
        return self.email