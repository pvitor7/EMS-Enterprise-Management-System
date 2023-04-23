
from pandas.tseries.offsets import Week
from datetime import datetime, date
import pandas as pd
from .models import ProjectsEmployees
from django.forms.models import model_to_dict


class CalculateTime:
    
    def completed_hours(self, total_value, completed_value, created_date=1):
        
        completed_hours = int(completed_value[0:-3])
        completed_minutes = int(completed_value[-2:])
        
        total_hours = int(total_value[0:-3]) - int(completed_hours)
        total_minutes = int(total_value[-2:]) - int(completed_minutes)
        # Corrige o valor dos minutos, se necessário
        
        if total_minutes >= 60:
            total_hours += 1
            total_minutes = total_minutes - 60
        
        if total_minutes < 0:
            total_hours -= 1
            total_minutes = total_minutes + 60
        
        if completed_hours > total_hours:
            return total_value;
        
        # Formata a saída
        if total_hours < 10:
            total_hours = f'0{total_hours}'

        if total_minutes < 10:
            total_minutes = f'0{total_minutes}'
        
        return f'{total_hours}:{total_minutes}'

    
    
    def calculate_hours_project(self, project, new_employee=None):
        employees_in_project = ProjectsEmployees.objects.filter(project=project)
        number_employees = len(employees_in_project)
        if new_employee:
            number_employees += 1
        
        today = pd.Timestamp.today().date();
        new_total_hours = project.last_hours;
        date_project_created = pd.Timestamp(project.created_at).date();
        
        number_days = (today - date_project_created).days
        #Soma das horas semanais de todos os funcionários envolvidos no projeto
        if number_employees > 0:
            for employee_in_project in employees_in_project:
                if employee_in_project.employee:
                    new_total_hours = CalculateTime.completed_hours(self, new_total_hours, employee_in_project.employee.weekly_workload)
        #####################################################################
        completed_hours = int(new_total_hours[0:-3])
        completed_minutes = int(new_total_hours[-2:])
        ####################################################################
        total_hours = float((int(project.last_hours[0:-3]) - completed_hours) / number_employees) * number_days
        total_minutes = (int(project.last_hours[-2:]) - completed_minutes)

        
        if total_minutes >= 60:
            total_hours = int(total_hours) + 1
            total_minutes = total_minutes - 60
            if total_minutes < 10:
                total_minutes = f'0{total_minutes}'

        elif total_minutes < 0:
            total_hours -= 1
            total_minutes += 60

        if total_hours < 0:
            total_hours = 0
            total_minutes = 0

        else:
            total_minutes = str(int(total_minutes))
            if len(total_minutes) == 1:
                total_minutes = f'0{total_minutes}'

        if completed_hours > total_hours:
            return project.last_hours;

        if total_hours < 10:
            total_hours = str(f'0{int(total_hours)}')
        else:
            total_hours = str(int(total_hours))
        
        return f'{total_hours}:{total_minutes}'

    
    def convert_days_hours_minutes(self, time):
        days=0;
        hours = int(time[0:-3]);
        minutes = int(time[-2:-1]);
        
        if hours > 8:
            days = float(hours/8) + 1;
            hours = hours%24;
            
        if hours < 10:
            hours = str(f'0{hours}')
        if minutes < 10:
            minutes = str(f'0{minutes}');
        
        if days:
            today = datetime.today().date();
            term = pd.bdate_range(today, periods=days);
            estimated_date = term[-1].date()
            return estimated_date
        
        return datetime.today().date()
        

    
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
        print("Model to dict aqui:", model_to_dict(project))
        print("Data aqui:", project.estimed_date, next_friday.date())
        
        if project.estimed_date > next_friday.date():
            project_hours_week = days_left * 8;
        else:
            calculate_week_project = pd.Timestamp(project.estimed_date).date() - today
            project_hours_week = int(calculate_week_project.days +  1) * 8;
        
        print("horas por semana aqui: ->:", project_hours_week, hours_worked)
        total_seconds = employee.weekly_workload.total_seconds()
        hours = round(total_seconds / 3600)
        
        accept_new_project =  (hours_worked + project_hours_week) < hours
        if accept_new_project:
            return True
        
        return False;
       
    
        
