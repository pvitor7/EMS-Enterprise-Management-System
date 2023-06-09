import uuid
from django.db import models
from departaments.models import Departament, RolesChoices
from employees.models import Employees
from datetime import timedelta


class Project(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    title = models.CharField(null=False, blank=False, max_length=48, unique=False)
    estimed_date = models.DateField(null=True, blank=True, default=None);
    date_last_estimate_calc = models.DateTimeField(auto_now=True)
    last_hours = models.DurationField(default=timedelta(seconds=0))
    completed_hours = models.DurationField(null=True, blank=True, default=timedelta(seconds=0))
    departament = models.ForeignKey(Departament, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProjectsEmployees(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    role = models.TextField(choices=RolesChoices.choices, default=RolesChoices.DEFAULT)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    employee = models.ForeignKey(Employees, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)