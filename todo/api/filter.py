import django_filters
from todo.models import Todo

class TodoFilter(django_filters.FilterSet):
    class Meta:
        model = Todo
        fields = {
            'completed': ['exact'],         
            'created_at': ['gte', 'lte'], 
            'updated_at': ['gte', 'lte'],
        }