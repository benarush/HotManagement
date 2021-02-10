from rest_framework import serializers
from .models import TaskDetail, Task

class TaskSerializer(serializers.ModelSerializer):
    # author = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = '__all__'

    # def get_author(self, obj):
    #     return obj.author.username


class SubTaskSerializer(serializers.ModelSerializer):
    task_parent = serializers.SerializerMethodField()
    current_status = serializers.SerializerMethodField()

    class Meta:
        model = TaskDetail
        fields = ("id", "problem", "mission", "responsibility", "email","current_status","task_parent")

    def get_task_parent(self, obj):
        return obj.task.problem

    def get_current_status(self, obj):
        return "Open" if obj.status==1 else "Closed" if obj.status== 0 else "Stuck"

    def create(self, validated_data):
        task = validated_data['task']
        status = validated_data['status']
        return TaskDetail.objects.create(
            task=task,
            problem=validated_data['problem'],
            mission=validated_data['mission'],
            status=status,
            email=validated_data['email'],
            responsibility=validated_data['responsibility'],
        )


class TaskWithDetailsSerializer(TaskSerializer):
    sub_tasks = SubTaskSerializer(source='taskdetail_set', read_only=True, many=True)

