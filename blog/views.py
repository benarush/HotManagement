from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.models import User
from .models import Post

from django.views.generic import (
    ListView ,
    DetailView,
    CreateView ,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin


class PostsListHome(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
#   Ordering from the oldest to the newest Data
    ordering = ['-date_posted']
    #   The paginate_by is to set how many posts will be in each page
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(PostsListHome, self).get_context_data(**kwargs)  # get the default context data
        context['latest_post'] = Post.objects.last()
        return context

class UserPostsListHome(ListView):
    model = Post
    template_name = "blog/user_post.html"
    context_object_name = "posts"
#   The paginate_by is to set how many posts will be in each page
    paginate_by = 5
    def get_context_data(self, **kwargs):
        context = super(UserPostsListHome, self).get_context_data(**kwargs)  # get the default context data
        context['latest_post'] = Post.objects.last()
        return context

#   The get_queryset func is used to edit the data we need
    def get_queryset(self):
#       the get_object_or_404 return 404 if the user dont exist , and if he exist it return his user object
        user = get_object_or_404(User , username = self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostsDetailsView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostsDetailsView, self).get_context_data(**kwargs)  # get the default context data
        context['latest_post'] = Post.objects.last()
        return context

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
#   The Field Variable Tell CreateView Class witch field that we want to update on the creation
    fields = ['title' , 'content']

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)  # get the default context data
        context['latest_post'] = Post.objects.last()
        return context

    def form_valid(self, form):
#       this will set the form instance author to the user that log in , in the request
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title' , 'content']
    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)  # get the default context data
        context['latest_post'] = Post.objects.last()
        return context

    def form_valid(self, form):
        #       this will set the form instance author to the user that log in , in the request
        form.instance.author = self.request.user
        return super().form_valid(form)

#   this method will check if the user author and the user that log in are same.
    def test_func(self):
#   The get_object() Will Get the object that we want to update.
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    context_object_name = "post"
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(PostDeleteView, self).get_context_data(**kwargs)  # get the default context data
        context['latest_post'] = Post.objects.last()
        return context

#   this method will check if the user author and the user that log in are same.
    def test_func(self):
#   The get_object() Will Get the object that we want to update.
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    context = {'title': 'About Me!',
               'latest_post':Post.objects.last()
               }
    return render(request, 'blog/about.html', context)

def mainPage(request):
    return render(request, 'blog/MainPage.html')
