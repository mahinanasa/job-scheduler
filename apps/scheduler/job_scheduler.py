import time
import environ
from celery import shared_task
from django.utils import timezone
from apps.jobs.models import Job

env = environ.Env()
environ.Env.read_env()

MAX_CONCURRENT_JOBS = env.MAX_CONCURRENT_JOBS

@shared_task
def process_jobs():
    running_jobs = Job.objects.filter(status='running').count()
    
    if running_jobs >= MAX_CONCURRENT_JOBS:
        return
    
    pending_jobs = Job.objects.filter(status='pending').order_by('-priority', 'deadline')[:MAX_CONCURRENT_JOBS - running_jobs]

    for job in pending_jobs:
        job.start()
        time.sleep(job.estimated_duration)  # Simulating job execution
        job.complete()
