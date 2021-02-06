from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from users import views as users_views
from django.contrib.auth import views as auth_views
from blog.models import Post
from blog.views import mainPage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', users_views.register , name = 'register'),
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html" , extra_context={'latest_post':Post.objects.last()} ), name = "login"),
    path('logout/' , auth_views.LogoutView.as_view(template_name="users/logout.html" , extra_context={'latest_post':Post.objects.last()} ), name = "logout" ),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="users/password_reset.html" , extra_context={'latest_post':Post.objects.last()}), name="password_reset"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html", extra_context={'latest_post':Post.objects.last()}),name="password_reset_confirm"),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html" , extra_context={'latest_post':Post.objects.last()}),name="password_reset_complete"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html" , extra_context={'latest_post':Post.objects.last()}),name="password_reset_done"),
    path('profile' , users_views.profile , name = "profile"),
    path('blog/', include('blog.urls')),
    path('tasks/', include('Tasks.urls')),
    path('', mainPage, name='Main'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
