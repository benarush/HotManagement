from django.urls import path
from .views import (
    PostsListHome ,
    about ,
    PostsDetailsView ,
    PostCreateView ,
    PostUpdateView ,
    PostDeleteView,
    UserPostsListHome,
    mainPage
    )

urlpatterns = [
    path('', PostsListHome.as_view(), name='blog-home'),
    path('user/<str:username>/', UserPostsListHome.as_view() ,name='user-posts'),
#   Here the int:pk its variable that django goin to grab from the url , we call it pk because its what DetailsView
#   expect to catch to get the specific item of post . if we call it other name , we will need to specified that to catch.
    path('post/<int:pk>/' ,PostsDetailsView.as_view() , name='post-details' ),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/create/' , PostCreateView.as_view() , name='post-create'),
    path('about/', about ,name='blog-about'),
]