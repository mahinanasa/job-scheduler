import time
from threading import Thread
from django.utils import timezone
from apps.jobs.models import Job  
from celery import shared_task
from queue import PriorityQueue
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

MAX_RUNNING_JOBS = 3  # Maximum number of jobs running at the same time
@shared_task
def process_jobs():

    # Priority Queue to store jobs
    pq = PriorityQueue()

    # Fetch all pending jobs
    jobs = Job.objects.filter(status='pending').order_by('priority_value')
    for job in jobs:
        priority = job.priority
        if job.deadline:
            # Use EDF (Earliest Deadline First) if there's a deadline
            priority = job.deadline.timestamp()  
        else:
            priority = job.priority_value
        
        print(f"Job {job.id} with priority: {priority}")
        pq.put((priority, job.id, job)) 
    
    running_jobs = Job.objects.filter(status='running').count()

    while not pq.empty() and running_jobs < MAX_RUNNING_JOBS:
        _, _, job = pq.get() 

        if job.status == 'pending':
            running_jobs += 1
            job_thread = Thread(target=simulate_job_execution, args=(job,))
            job_thread.start()
            job_thread.join()  
            running_jobs -= 1

    # Simulate job execution
def simulate_job_execution(job):
    try:
        print(f"simulate_job_execution - Job {job.id} with priority: {job.priority}")

        job.status = 'running'
        job.start_time = timezone.now()
        job.save()
        send_job_update(job) 
        # Simulate job execution
        time.sleep(job.estimated_duration) 

        job.status = 'completed'
        job.end_time = timezone.now()
        job.save()
        send_job_update(job) 

    except Exception as e:
        job.status = 'failed'
        job.save()
        send_job_update(job) 
        
def send_job_update(job):
    """Notify WebSocket clients about job status updates"""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "job_updates",
        {
            "type": "send_job_status",
            "job": {
                "id": job.id,
                "status": job.status
            },
        },
    )            