import uuid
from django.db import models
from departaments.models import Departament, RolesChoices
from employees.models import Employees


class Project(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    title = models.CharField(null=False, blank=False, max_length=48, unique=False)
    estimed_hours = models.TimeField(default=0)
    last_hours = models.TimeField(default=0)
    departament = models.ForeignKey(Departament, on_delete=models.PROTECT, null=True, blank=True)


class ProjectsEmployees(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    role = models.TextField(choices=RolesChoices.choices, default=RolesChoices.DEFAULT)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, null=True, blank=True)