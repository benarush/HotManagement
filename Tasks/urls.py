from django.urls import path
from .views import home , AllTasksViews

urlpatterns = [
    path('', home ,name='blog-home'),
    path('alltasks/', AllTasksViews.as_view() , name='all-tasks'),

]