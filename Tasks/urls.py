from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='task-home'),
    path('alltasks/create_task/' , TaskCreateView.as_view(), name="create-task"),
    path('alltasks/edit_task/<int:pk>', TaskUpdateView.as_view(), name='edit-task'),
    path('alltasks/details_task/<int:pk>', TaskDetailsView.as_view(), name="task-details"),
    path('alltasks/create_details_task/<int:pk>', TaskDetailsCreateView.as_view(), name = 'create-task-details'),
    path('alltasks/delete_task/<int:pk>', TaskDeleteView.as_view(), name="delete-task"),
    path('alltasks/', AllTasksViews.as_view(), name='all-tasks')
]
