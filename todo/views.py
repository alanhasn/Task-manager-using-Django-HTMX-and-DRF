# ======= IMPORTS =======
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseNotAllowed
from django.shortcuts import HttpResponse, get_object_or_404, render
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.base import TemplateView

from .forms import TaskForm
from .models import Todo

# ====== VIEWS =======

class ListTaskView(LoginRequiredMixin, ListView):
    """Display a list of tasks for the logged-in user, with optional filtering and HTMX support."""

    model = Todo
    context_object_name = "todos"
    template_name = "todos/todo.html"

    def render_to_response(self, context, **response_kwargs):
        """Return partial template if HTMX request, otherwise return full page."""
        if self.request.headers.get("HX-Request") == "true":
            return render(self.request, "todos/partials/table-rows.html", {"todos": context["todos"]})
        return super().render_to_response(context, **response_kwargs)

    def get_queryset(self):
        """Filter tasks by user and query params (completed/uncompleted)."""
        queryset = Todo.objects.filter(user=self.request.user)
        value_param = self.request.GET.get("filter")
        if value_param == "completed":
            queryset = queryset.filter(completed=True)
        elif value_param == "uncompleted":
            queryset = queryset.filter(completed=False)
        return queryset

    def get_context_data(self, **kwargs):
        """Inject task creation form into the context."""
        context = super().get_context_data(**kwargs)
        context["form"] = TaskForm
        return context

class CreateTaskView(LoginRequiredMixin, CreateView):
    """Create a new task and return HTMX partials for success or validation errors."""

    model = Todo
    form_class = TaskForm
    template_name = "todos/partials/add-task-modal.html"

    def form_valid(self, form):
        """Assign user to task, save it, and return rendered row with success trigger."""
        task = form.save(commit=False)
        task.user = self.request.user
        task.save()

        response = render(self.request, "todos/partials/table-row.html", {"todo": task})
        response["HX-Trigger"] = "success"
        return response

    def form_invalid(self, form):
        """Return modal with validation errors and HTMX fail trigger."""
        response = render(self.request, "todos/partials/add-task-modal.html", {"form": form})
        response["HX-Retarget"] = "#add-todo-modal"
        response["HX-Reswap"] = "outerHTML"
        response["HX-Trigger-After-Settle"] = "fail"
        return response
    
class EditTaskView(LoginRequiredMixin, UpdateView):
    """Edit an existing task and return HTMX partials for update or errors."""

    model = Todo
    context_object_name = "todo"
    form_class = TaskForm
    pk_url_kwarg = "pk"
    template_name = "todos/partials/edit-task-modal.html"

    def get_queryset(self):
        """Restrict edit access to tasks owned by the current user."""
        return Todo.objects.filter(user=self.request.user)

    def form_valid(self, form):
        """Save edited task and return updated row with HTMX trigger."""
        todo = form.save()
        response = render(self.request, "todos/partials/table-row.html", {"todo": todo})
        response["HX-Trigger"] = "task-edited"
        return response

    def form_invalid(self, form):
        """Return modal with validation errors and HTMX fail trigger."""
        response = render(self.request, self.template_name, {"form": form, "todo": self.get_object()})
        response["HX-Retarget"] = "#edit-todo-modal"
        response["HX-Reswap"] = "outerHTML"
        response["HX-Trigger-After-Settle"] = "fail"
        return response
    
class UpdateTaskStatusView(LoginRequiredMixin, View):
    """Toggle the completion status of a task (complete/incomplete)."""

    def post(self, request, pk):
        """Toggle task status and return updated row or full page."""
        todo = get_object_or_404(Todo, user=request.user, pk=pk)
        todo.completed = not todo.completed
        todo.save()

        if request.headers.get("HX-Request") == "true":
            return render(request, "todos/partials/table-row.html", {"todo": todo})
        todos = Todo.objects.filter(user=request.user)
        return render(request, "todos/todo.html", {"todos": todos})

    def get(self, request):
        """Block GET requests; only POST is allowed."""
        return HttpResponseNotAllowed(["POST"])
    
class DeleteTaskView(LoginRequiredMixin, View):
    """Delete a task via HTMX request."""

    def delete(self, request, pk):
        """Delete the task and return an empty HTMX success response."""
        todo = get_object_or_404(Todo, pk=pk, user=request.user)
        todo.delete()
        response = HttpResponse(status=204)
        response["HX-Trigger"] = "task-deleted"
        return response

    def dispatch(self, request, *args, **kwargs):
        """Allow only DELETE requests."""
        if request.method != "DELETE":
            return HttpResponseNotAllowed(["DELETE"])
        return super().dispatch(request, *args, **kwargs)

class SearchTaskView(LoginRequiredMixin, ListView):
    """Search tasks by title for the current user."""

    model = Todo
    context_object_name = "todos"
    template_name = "todos/partials/table-rows.html"

    def get_queryset(self):
        """Return tasks matching the search query."""
        query = self.request.GET.get("search")
        if query:
            return self.request.user.todos.filter(Q(title__icontains=query))
        return self.request.user.todos.all()

class AboutMePageView(TemplateView):
    """Static About Me page."""
    template_name = "todos/about-me.html"
