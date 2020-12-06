from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Post._meta.get_fields() if f.one_to_many != True]
    search_fields = ('author__username',)


#admin.site.register(Post)
