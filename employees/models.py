import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class Gender(models.TextChoices):
    DEFAULT = "Not informed"
    MALE = "Male"
    FELAME = "Female"
    NONBINARY = "Nonbinary"
    AGENDER = "Agender"
    OTHER = "Other"

class DriverLicense(models.TextChoices):
    DEFAULT = "Not informed"
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    AB = "AB"
    AC = "AC"
    AD = "AD"
    AE = "AE"


class Employees(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(null=False, blank=False, max_length=128)
    cpf = models.CharField(null=False, blank=False, max_length=11, unique=True)
    rg = models.CharField(unique=True, null=False, blank=False, max_length=9)
    gender = models.TextField(choices=Gender.choices, default=Gender.DEFAULT)
    driver_license = models.TextField(choices=DriverLicense.choices, default=DriverLicense.DEFAULT)
    birth_date = models.DateField(null=False, blank=False)
    salary = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    weekly_hours = models.TimeField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
