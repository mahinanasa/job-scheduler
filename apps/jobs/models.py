from django.db import models
from django.utils import timezone
from apps.users.models import AppUser  

class Job(models.Model):
    PRIORITY_CHOICES = [('high', 'High'), ('medium', 'Medium'), ('low', 'Low')]
    STATUS_CHOICES = [('pending', 'Pending'), ('running', 'Running'), ('completed', 'Completed'), ('failed', 'Failed')]

    name = models.CharField(max_length=255)
    estimated_duration = models.PositiveIntegerField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES,  default='low')
    deadline = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)  
    priority_value = models.IntegerField(default=3) # 1: High, 2: Medium, 3: Low

    def start(self):
        self.status = 'running'
        self.start_time = timezone.now()
        self.save()

    def complete(self):
        self.status = 'completed'
        self.end_time = timezone.now()
        self.save()

    def __str__(self):
        return self.name
