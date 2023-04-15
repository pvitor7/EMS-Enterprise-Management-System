
from datetime import datetime, timedelta, date
import pandas as pd

class CalculateTime:
    
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
        