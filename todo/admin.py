from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    '''Admin View for Todo model'''

    list_display = ('title','user','created_at','updated_at')
    list_filter = ('user__username',)
    search_fields = ("user__username","title__icontains")
    ordering = ('-created_at',)