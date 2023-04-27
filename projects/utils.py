
from pandas.tseries.offsets import Week
from datetime import date, timedelta, time, datetime
import pandas as pd
from .models import ProjectsEmployees
from django.forms.models import model_to_dict
import math
from django.utils import timezone



class CalculateTime:
    
    def str_to_timedelta(self, time_str):
        if isinstance(time_str, str):
            hours, minutes = time_str.split(":")
            total_minutes = int(hours) * 60 + int(minutes)
        else:
            total_minutes = int(time_str) * 60

        days = total_minutes // (24 * 60)
        minutes = total_minutes % 60
        hours = (total_minutes // 60) % 24
        return timedelta(days=days, hours=hours, minutes=minutes)
    
    
    #converte o período de datatime.time para instring em quantidade de horas
    def timedelta_to_str(self, timedelta_obj):
        if timedelta_obj is None:
            return "00:00"
        total_seconds = int(timedelta_obj.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours:02d}:{minutes:02d}"


    #calcula as horas completas no projeto
    def calculate_hours_project(self, project, new_employee=None):
        employees_in_project = ProjectsEmployees.objects.filter(project=project)
        number_employees = len(employees_in_project)
        
        if new_employee:
            number_employees += 1
        
        if number_employees > 0:
            new_total_hours = sum([
                (timezone.now() - timezone.localtime(emp.employee.created_at)).days * 8
                for emp in employees_in_project if emp.employee
            ])
        else:
            new_total_hours = 0
        
        if new_total_hours == 0:
            return timedelta(seconds=0)
        elif new_total_hours > project.last_hours.total_seconds() / 3600:
            return project.last_hours
        else:
            return timedelta(hours=new_total_hours)

    #faz a estimativa de data de conclusão baseada nas horas do projeto e data inicial
    def convert_days_hours_minutes(self, time_delta_str, time_start=date.today()):
        if isinstance(time_delta_str, str):
            # Separe as horas e minutos
            hours, minutes = time_delta_str.split(":")
            # Converta as horas para minutos
            total_minutes = int(hours) * 60 + int(minutes)
            # Crie um objeto timedelta usando o total de minutos
            time_delta_str = timedelta(minutes=total_minutes)
            
        total_hours = time_delta_str.seconds // 3600 + time_delta_str.days * 24
        
        days = math.ceil(total_hours / 8)
        time_start_str = time_start.strftime("%Y-%m-%d %H:%M:%S")
        time_start = datetime.strptime(time_start_str, "%Y-%m-%d %H:%M:%S")
        bdays = pd.bdate_range(start=time_start, periods=days)

        if len(bdays) == 0:
            return date.today()
        estimated_date = bdays[-1].date()
        return estimated_date
    
  
    def get_next_project(self, project, employee):
        #calculando a ultima segunda e proxima sexta-feira
        today = pd.Timestamp.today().date()
        last_monday = (today - Week(weekday=0)).date()
        next_friday = pd.Timestamp(today + Week(weekday=4))
        days_left = int((next_friday - pd.Timestamp.today()).days);

        #reunindo todos os projetos que o funcionário trabalha
        hours_worked = 0;
        projects_employee = ProjectsEmployees.objects.filter(employee=employee);
        for projects_employee in projects_employee:
            #calculando as horas que o projeto tem dentro da semana
            if projects_employee.project.estimed_date > next_friday.date():
                hours_worked = (days_left) * 8;
            else:
                difference = (next_friday.date() - pd.Timestamp(projects_employee.project.estimed_date).date())
                hours_worked = int(difference.days +  1) * 8;

        #verificando se as horas a trabalhar na semana mais as horas do novo projeto até o final de semana ultrapassarão as hora permitidas para o funcionário.
        project_hours_week = 0
        
        if project.estimed_date > next_friday.date():
            project_hours_week = days_left * 8;
        else:
            calculate_week_project = pd.Timestamp(project.estimed_date).date() - today
            project_hours_week = int(calculate_week_project.days +  1) * 8;
        
        total_seconds = employee.weekly_workload.total_seconds()
        hours = round(total_seconds / 3600)
        
        accept_new_project =  (hours_worked + project_hours_week) < hours
        if accept_new_project:
            return True
        
        return False;
       
    
        
