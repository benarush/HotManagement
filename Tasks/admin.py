from django.contrib import admin
from .models import Task, TaskDetail, FullReport


@admin.register(Task)
class MyTasksAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Task._meta.get_fields() if f.one_to_many != True]
    search_fields = ('author__username',)


@admin.register(TaskDetail)
class MyTasksDetailsAdmin(admin.ModelAdmin):
    list_display = [f.name for f in TaskDetail._meta.get_fields() if f.one_to_many != True]
    search_fields = ('author__username',)


@admin.register(FullReport)
class FullReportAdmin(admin.ModelAdmin):
    list_display = [f.name for f in FullReport._meta.get_fields() if f.one_to_many != True]
    search_fields = ('owner__username', 'file_path')
