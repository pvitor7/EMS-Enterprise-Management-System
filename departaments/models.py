import uuid
from django.db import models
from employees.models import Employees

class RolesChoices(models.TextChoices):
    DEFAULT = "Employee"
    SUPERVISOR = "Supervisor"

class Departament(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    title = models.CharField(null=False, blank=False, max_length=48, unique=True)


class Roles(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    role = models.TextField(choices=RolesChoices.choices, default=RolesChoices.DEFAULT)
    # worked_hours = models.TimeField(default=0)
    departament = models.ForeignKey(Departament, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, null=True, blank=True)