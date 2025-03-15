
import environ
import traceback  
from django.shortcuts import render, redirect
from .models import Job
from django.contrib.auth.decorators import login_required
from threading import Thread
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import make_aware, now
from .serializers import JobSerializer, JobSubmitSerializer
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Count
from apps.scheduler.tasks import process_jobs

env = environ.Env()
environ.Env.read_env()

MAX_RUNNING_JOBS = env.int('MAX_RUNNING_JOBS', default=3)
PRIORITY_MAP = {'high': 1, 'medium': 2, 'low': 3} 

@login_required
def dashboard(request):
    jobs_list = Job.objects.filter(user=request.user).order_by('-id')
    paginator = Paginator(jobs_list, 10)
    page_number = request.GET.get('page')
    jobs = paginator.get_page(page_number)

    job_counts = jobs_list.values('status').annotate(count=Count('status'))
    grouped_jobs = {status: 0 for status in ['pending', 'running', 'completed']}  

    for entry in job_counts:
        grouped_jobs[entry['status']] += entry['count']

    completed_jobs = jobs_list.filter(status='completed')

    total_wait_time = sum((job.end_time - job.start_time).total_seconds() for job in completed_jobs if job.start_time and job.end_time) 
    avg_wait_time = total_wait_time / len(completed_jobs) if completed_jobs else 0

    priority_count = {
        'high': jobs_list.filter(priority='high').count(),
        'medium': jobs_list.filter(priority='medium').count(),
        'low': jobs_list.filter(priority='low').count(),
    }
    return render(request, 'jobs/dashboard.html', {
        'jobs': jobs,
        'grouped_jobs': grouped_jobs,
        'avg_wait_time': avg_wait_time,
        'priority_count': priority_count
    })          

@login_required
def submitJob(request):
    if request.method == 'POST':
        name = request.POST['name']
        priority = request.POST['priority']
        estimated_duration = int(request.POST['estimated_duration'])
        deadline = request.POST['deadline'] if 'deadline' in request.POST else None
        priority_value = set_priority_value(priority)

        # Create the job
        job = Job.objects.create(
            name=name,
            priority=priority,
            estimated_duration=estimated_duration,
            status='pending',
            user=request.user,
            deadline=deadline if deadline else None,
            priority_value=priority_value
        )
        # Start the job processing thread asychronously
        # job_thread = Thread(target=process_jobs)
        # job_thread.start()

        return redirect('jobs:dashboard')

    return render(request, 'jobs/create_job.html')

def set_priority_value(priority):
    if priority == 'high':
          return 1
    elif priority == 'medium':
          return 2
    else:
           return 3


# API Definitions
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_api_job(request):
    try:
        serializer = JobSubmitSerializer(data=request.data)
        if serializer.is_valid():
            jobData = serializer.validated_data
            priority = jobData.get('priority', 'low') 
            priority_value = set_priority_value(priority)
            job = serializer.save(user=request.user, status='pending', priority_value=priority_value)
            # Start job processing asynchronously
            # job_thread = Thread(target=process_jobs)
            # job_thread.start()
            return Response(
                {'message': 'Job submitted successfully!', 'job_id': job.id},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Error in create_api_job:", e)  
        traceback.print_exc() 
        return Response(
            {'error': 'Something went wrong. Please try again.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def job_status(request, job_id):
    """API to fetch the status of a specific job."""
    try:
        job = Job.objects.get(id=job_id, user=request.user)
        serializer = JobSerializer(job)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Job.DoesNotExist:
        return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_jobs(request):
    """API to list all jobs for the authenticated user."""
    jobs = Job.objects.filter(user=request.user)
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

