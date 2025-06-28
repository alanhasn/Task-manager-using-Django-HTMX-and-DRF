from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseNotAllowed
from django.shortcuts import HttpResponse, get_object_or_404 , render
from django.views.decorators.http import require_http_methods
from .models import Todo
from .forms import TaskForm


@login_required(login_url='/admin/login/')
def list_task(request):
    form = TaskForm()
    
    # Filter tasks
    value_param = request.GET.get("filter")
    if value_param == "completed":
        todos = Todo.objects.filter(user=request.user, completed=True)
    elif value_param == "uncompleted":
        todos = Todo.objects.filter(user=request.user, completed=False)
    else:
        todos = Todo.objects.all().filter(user=request.user)

    # if request is HTMX Request
    if request.headers.get("HX-Request") == "true": 
        return render(request, "todos/partials/table-rows.html", {"todos": todos}) # send a partials table rows

    return render(request, "todos/todo.html", {"todos": todos,"form":form})

@login_required(login_url='/admin/login/')
@require_http_methods(["GET", "POST"])
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

            response = render(request , "todos/partials/table-row.html" , {"todo":task})
            response['HX-Trigger'] = 'success'  
            return response
        else:
            response = render(request , "todos/partials/add-task-modal.html" , {"form":form})
            response['HX-Retarget'] = '#add-todo-modal'
            response['HX-Reswap'] = 'outerHTML'
            response['HX-Trigger-After-Settle'] = 'fail'
            return response
    else:
        form = TaskForm()
        return render(request , "todos/partials/add-task-modal.html" , {"form":form})

@login_required(login_url='/admin/login/')
@require_http_methods(["GET", "POST"])
def edit_task(request , pk):
    todo = get_object_or_404(Todo , pk=pk , user=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST , instance=todo)

        if form.is_valid():
            title = form.cleaned_data.get("title")
            description = form.cleaned_data.get("description")

            todo.title = title
            todo.description = description
            todo.save()
            response = render(request , "todos/partials/table-row.html" , {'todo':todo})
            response["HX-Trigger"] = "task-edited" # add task-edited HTMX trigger in the response
            return response
        else:
            response = render(request , "todos/partials/edit-task-modal.html" , {"form":form , "todo":todo})
            response['HX-Retarget'] = '#edit-todo-modal'
            response['HX-Reswap'] = 'outerHTML'
            response['HX-Trigger-After-Settle'] = 'fail'
            return response
    else:
        form = TaskForm(instance=todo)
        
        return render(request , "todos/partials/edit-task-modal.html" , {"form":form , "todo":todo})
        

@login_required
@require_http_methods(["POST"])
# Function for check the task as completed
def check(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save()

    if request.headers.get("HX-Request") == "true":
        return render(request, "todos/partials/table-row.html", {"todo": todo})
    
    todos = Todo.objects.all()
    return render(request, "todos/todo.html", {"todos": todos})

@login_required
@require_http_methods(["DELETE"])
# view for delete task
def delete_task(request, pk):
    if request.method != "DELETE":
        return HttpResponseNotAllowed(["DELETE"])

    todo = get_object_or_404(Todo, pk=pk , user=request.user)
    todo.delete()
    response =  HttpResponse(status=204)
    response["HX-Trigger"] = "task-deleted" # add task-deleted HTMX trigger in the response
    return response

@login_required(login_url='/admin/login/')
def search(request):
    import time
    time.sleep(1)

    query = request.GET.get("search")

    todos = request.user.todos.filter(
        Q(title__icontains=query)
    )
    return render(request , "todos/partials/table-rows.html" , {"todos":todos})