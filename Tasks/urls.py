from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='blog-home'),
    path('alltasks/create_task/' , TaskCreateView.as_view(), name="create_task"),
    path('alltasks/edit_task/<int:pk>', TaskUpdateView.as_view(), name='edit-task'),
    path('alltasks/details_task/<int:pk>', TaskDetailsView.as_view(), name="task-details"),
    path('alltasks/delete_task/<int:pk>', TaskDeleteView.as_view(), name="delete-task"),
    path('alltasks/', AllTasksViews.as_view(), name='all-tasks')
]
