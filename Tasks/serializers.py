from rest_framework import serializers
from .models import TaskDetail , Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskDetail
        fields = '__all__'