from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'  

class JobSubmitSerializer(serializers.ModelSerializer):
    """Serializer for submitting new jobs (excluding start_time & end_time)."""
    
    class Meta:
        model = Job
        fields = ['name', 'priority', 'estimated_duration']
