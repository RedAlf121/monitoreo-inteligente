from . import TIME_DEFAULT,LOG_PATH,LOG_FORMAT
import schedule
from datetime import datetime
import pickle
import time
import os
from pathlib import Path

# Convertir a ruta absoluta si es necesario
LOG_PATH_ABSOLUTE = os.path.abspath(LOG_PATH)

def execute_scheduled_task(scheduling_method, task_function, testing=False):
    if not has_task_run_today() or testing:
        if not is_time_past_default_execution_time():
            execute_and_log_task(task_function)
        scheduling_method(lambda: execute_and_log_task(task_function))
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        print("Task already run today")

def start_test_schedule(task_function):
    execute_scheduled_task(configure_minute_schedule, task_function, testing=True)

def start_daily_schedule(task_function):
    execute_scheduled_task(configure_daily_schedule, task_function)

def configure_daily_schedule(task_function):
    schedule.every().days.at(TIME_DEFAULT).do(task_function)

def configure_minute_schedule(task_function):
    schedule.every().minutes.do(task_function)

def is_time_past_default_execution_time():
    time_format = '%H:%M'
    current_time_str = datetime.now().strftime(time_format)
    current_time_datetime = datetime.now().strptime(current_time_str, time_format)
    default_time_datetime = datetime.now().strptime(TIME_DEFAULT, time_format)
    return current_time_datetime > default_time_datetime

def execute_and_log_task(task_function):
    current_execution_time = datetime.now().strftime(LOG_FORMAT)
    task_function()
    
    # Asegurar que el directorio exista
    os.makedirs(os.path.dirname(LOG_PATH_ABSOLUTE), exist_ok=True)
    
    with open(LOG_PATH_ABSOLUTE, 'wb') as log_file:
        pickle.dump(current_execution_time, log_file)

def has_task_run_today():
    try:
        if not os.path.exists(LOG_PATH_ABSOLUTE):
            return False
            
        with open(LOG_PATH_ABSOLUTE, 'rb') as log_file:
            last_execution_date = pickle.load(log_file)
            current_date = datetime.now().strftime(LOG_FORMAT)
        return last_execution_date == current_date
    except (EOFError, FileNotFoundError):
        return False 


