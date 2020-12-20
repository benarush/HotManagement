from django.urls import path
from .views import *
from .apiView import *

urlpatterns = [
    path('', home, name='task-home'),
    path('alltasks/create_task/' , TaskCreateView.as_view(), name="create-task"),
    path('alltasks/edit_task/<int:pk>', TaskUpdateView.as_view(), name='edit-task'),
    path('alltasks/details_task/<int:pk>', TaskDetailsView.as_view(), name="task-details"),
    path('alltasks/create_details_task/<int:pk>', TaskDetailsCreateView.as_view(), name = 'create-task-details'),
    path('alltasks/delete_task/<int:pk>', TaskDeleteView.as_view(), name="delete-task"),
    path('alltasks/api/', apiOverview , name="api-overview"),
    path('alltasks/api/task_info/<str:pk>', task_info , name="task-info"),
    path('alltasks/api/sub_task_edit/', sub_task_edit, name="sub-task-edit"),
    path('alltasks/api/sub_task_delete/', sub_task_delete, name="sub-task-delete"),
    path('alltasks/api/sub_task_create/', sub_task_create, name="sub-task-create"),
    path('alltasks/', AllTasksViews.as_view(), name='all-tasks')
]
