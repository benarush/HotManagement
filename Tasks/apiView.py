from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Task, TaskDetail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *


@login_required
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Get specific task info': '/tasks/alltasks/api/task_info/<str:pk>',
        'Get all sub tasks for a specific task': '/tasks/alltasks/api/sub_tasks/<str>',
    }
    return Response(api_urls)


@login_required
@api_view(['GET'])
def task_info(request,pk):
    try:
        task = Task.objects.get(id=pk)
    except:
        context = {"status": "failed" ,"error": "no such of task", "data": None, "subtasks": None}
        return Response(context)
    if request.user != task.author:
        return Response({"status": "failed" ,"error": "permission denied", "data": None, "subtasks": None})
    task_serializer = TaskSerializer(task, many=False)
    sub_task = SubTaskSerializer(task.taskdetail_set.all(),many=True)
    context = {
        "status": "Success",
        "error": None,
        "data": {"task": task_serializer.data},
        "subtasks": sub_task.data
    }
    return Response(context)


@login_required
@api_view(['GET'])
def sub_tasks_data(request,task_pk):
    try:
        task = Task.objects.get(id=task_pk)
    except:
        return Response({"status": "failed" ,"error": "no such of task", "data": None, "subtasks": None})
    if request.user != task.author:
        return Response({"status": "failed" ,"error": "permission denied", "data": None, "subtasks": None})
    sub_task = SubTaskSerializer(task.taskdetail_set.all(), many=True)
    context = {
        "status": "Success",
        "error": None,
        "data": sub_task.data,
    }
    return Response(context)


@login_required
@csrf_exempt
def sub_task_edit(request):
    id = request.POST.get('id', '')
    type = request.POST.get('type', '')
    value = request.POST.get('value', '')
    sub_task = TaskDetail.objects.get(id=id)
    if type == "problem":
        sub_task.problem = value
    if type == "email":
        sub_task.email = value
    if type == "mission":
        sub_task.mission = value
    if type == "responsibility":
        sub_task.responsibility = value
    if type == "status":
        sub_task.status = True if value == "open" else False

    sub_task.save()
    return JsonResponse({"success": "Updated"})

@csrf_exempt
def sub_task_delete(request):
    id = request.POST.get('id', '')
    sub_task = TaskDetail.objects.get(id=id)
    sub_task.delete()
    return JsonResponse({"success": "sub task delete"})

@login_required
@csrf_exempt
def sub_task_create(request):
    task = Task.objects.get(id=request.POST.get('task_id', ''))
    if task.author != request.user:
        return JsonResponse({"message": "Permission Denied!"}, status=500)
    email = request.POST.get('email', '')
    problem = request.POST.get('problem', '')
    mission = request.POST.get('mission', '')
    responsibility = request.POST.get('responsibility', '')
    status = True if request.POST.get('status', '') == "open" else False
    print(f"task:{task}\nemail:{email}\nproblem:{problem}\nmission:{mission}\nstatus:{status}")
    try:
        sub_task_serializer = SubTaskSerializer(data=request.POST)
        if sub_task_serializer.is_valid(raise_exception=True):
            t = sub_task_serializer.save(task=task, status=status)
            return JsonResponse(sub_task_serializer.data)
    except Exception as e:
        print({"message": e})
        return JsonResponse(e.detail,status=500)
    return JsonResponse({"success": "sub task created !!"})
