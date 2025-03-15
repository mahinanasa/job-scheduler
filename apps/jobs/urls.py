from django.urls import path
from .views import dashboard,submitJob,create_api_job, job_status, list_jobs  
from rest_framework.authtoken.views import obtain_auth_token 

app_name = 'jobs'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('submit-job/', submitJob, name='submit-job'),
    path('create-job', create_api_job, name='create_api_job'),
    path('job-status/<int:job_id>', job_status, name='job-status'),
    path('list-jobs', list_jobs, name='list-jobs'),
    path('api-token-auth', obtain_auth_token, name='api_token_auth'),  # Token endpoint for API authentication

]
