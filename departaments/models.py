import uuid
from django.db import models

class RolesChoices(models.TextChoices):
    DEFAULT = "Employee"
    SUPERVISOR = "Supervisor"

class Departament(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    title = models.CharField(null=False, blank=False, max_length=48, unique=True)


class Roles(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    role = models.IntegerField(choices=RolesChoices.choices, default=RolesChoices.DEFAULT)
    departament = models.ForeignKey(Departament, on_delete=models.CASCADE, null=False)
    # employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=False)