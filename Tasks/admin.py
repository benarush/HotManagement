from django.contrib import admin
from .models import Task , TaskDetail


@admin.register(Task)
class MyTasksAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Task._meta.get_fields() if f.one_to_many != True]
    search_fields = ('author__username',)

admin.site.register(TaskDetail)


