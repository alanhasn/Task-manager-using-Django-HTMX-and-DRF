from django import forms
from .models import Todo
from django.core.exceptions import ValidationError

class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = [
            "title",
            "description"
        ]
    
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Add title"
    })
    )
    
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "textarea textarea-bordered w-full",
            "placeholder": "Add description",
            "rows": 6,
        })
    )

    def clean_title(self):
        title = self.cleaned_data.get('title')
        
        if len(title) < 5:
            raise ValidationError("The title is too short!")
        elif len(title) > 60:
            raise ValidationError("the title should be smaller than 60 character")
        
        return title
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        
        if len(description) < 20:
            raise ValidationError("The description is too short!")
        elif len(description) > 100:
            raise ValidationError("the description should be smaller than 100 character")
        
        return description