from crontab import CronTab
from datetime import datetime

def create_daily_cron_job(time_str, command):
    # Parse the time string to hours and minutes
    time = datetime.strptime(time_str, "%H:%M").time()
    # Access the current user's crontab
    cron = CronTab(user=True)
    # Create a new job
    job = cron.new(command=command)
    
    # Set the time for the job to run daily
    job.minute.on(time.minute)
    job.hour.on(time.hour)
    
    # Write the job to the crontab
    cron.write()
    print(f"Cron job created to run '{command}' daily at {time_str}")

def delete_all_cron_jobs(): # deletes all cron jobs
    cron = CronTab(user=True)
    cron.remove_all()
    cron.write()
    print("All cron jobs deleted")

def delete_cron_job(command): # command is the command to delete
    cron = CronTab(user=True)
    cron.remove_all(command=command)
    cron.write()
    print(f"Cron job '{command}' deleted")


# Example usage
time_to_run = "22:12"
command_to_run = "./scheduleCron.sh"

# Call the function with command and time
delete_all_cron_jobs()
create_daily_cron_job(time_to_run, command_to_run)
