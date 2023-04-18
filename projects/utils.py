
from pandas.tseries.offsets import Week
from datetime import datetime, timedelta, date, time
import pandas as pd
from .models import ProjectsEmployees

class CalculateTime:
    
    def get_next_project(self, project, employee):
        #calculando a ultima segunda e proxima sexta-feira
        today = pd.Timestamp.today().date()
        last_monday = (today - Week(weekday=0)).date()
        next_friday = pd.Timestamp(today + Week(weekday=4))
        days_left = (next_friday - pd.Timestamp.today()).days

        #reunindo todos os projetos que o funcionário trabalha
        hours_worked = 0;
        projects_employee = ProjectsEmployees.objects.filter(employee=employee);
        for projects_employee in projects_employee:
            #calculando as horas que o projeto tem dentro da semana
            if projects_employee.project.estimed_date > next_friday.date():
                hours_worked = (days_left + 1) * 8;
            
            else:
                difference = (next_friday.date() - pd.Timestamp(projects_employee.project.estimed_date).date())
                hours_worked = int(difference.days +  1) * 8;

        #verificando se as horas a trabalhar na semana mais as horas do novo projeto até o final de semana ultrapassarão as hora permitidas para o funcionário.
        project_hours_week = 0
        if project.estimed_date > next_friday.date():
            project_hours_week = (days_left + 1) * 8;
    
        else:
            calculate_week_project = pd.Timestamp(project.estimed_date).date() - today
            project_hours_week = int(calculate_week_project.days +  1) * 8;
           
                
        accept_new_project =  (hours_worked + project_hours_week) < int(employee.weekly_workload[:-3])
        if accept_new_project:
            return True
        
        return False;

        
    
    
    def calc_hours(self, total_value, completed_value):
        completed_hours = int(completed_value[0:-3]);
        completed_minutes = int(completed_value[-2:-1]);
        
        total_hours = int(total_value[0:-3]) - completed_hours;
        total_minutes = int(total_value[-2:-1]) - completed_minutes;
        
        if total_hours < 10:
                total_hours = str(f'0{total_hours}')
        if total_minutes < 10:
            total_minutes = str(f'0{total_minutes}');
        
        return f'{total_hours}:{total_minutes}';
        
    
    def convert_days_hours_minutes(self, time):
        days=0;
        hours = int(time[0:-3]);
        minutes = int(time[-2:-1]);
        
        if hours > 8:
            days = round(hours/8);
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
        