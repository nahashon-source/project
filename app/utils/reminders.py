from datetime import datetime, timedelta
from app.models import Donation
from app import db
import schedule
import threading
import time

def schedule_donation_reminder(donation):
    """Schedule a reminder for recurring donations"""
    if not donation.is_recurring:
        return
    
    intervals = {
        'monthly': 30,
        'quarterly': 90,
        'yearly': 365
    }
    
    days = intervals.get(donation.recurring_interval)
    if not days:
        return
        
    next_donation_date = datetime.utcnow() + timedelta(days=days)
    
    # Store next donation date in database
    donation.next_donation_date = next_donation_date
    db.session.commit()
    
    # Schedule reminder (implementation depends on your notification system)
    schedule_reminder_task(donation, next_donation_date)

def schedule_reminder_task(donation, reminder_date):
    """
    Schedule a reminder task using the schedule library
    This is a simple implementation - in production you'd want to use
    a proper task queue like Celery
    """
    def reminder_job():
        send_reminder_notification(donation)
    
    schedule.every().day.at("10:00").do(
        reminder_job
    ).tag(f'donation_{donation.id}')
    
def send_reminder_notification(donation):
    """
    Send reminder notification to donor
    Implementation depends on your notification system (email, push, etc)
    """
    # Example implementation - replace with your notification system
    print(f"Sending reminder for donation {donation.id}")
    
def run_scheduler():
    """Run the scheduler in a background thread"""
    while True:
        schedule.run_pending()
        time.sleep(60)
        
# Start the scheduler in a background thread
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()