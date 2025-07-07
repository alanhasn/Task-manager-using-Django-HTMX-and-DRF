from django.shortcuts import render


class RestrictAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/admin/") and hasattr(request, "user"):
            if not request.user.is_authenticated or not request.user.is_staff:

                return render(request, "account/403.html", status=403)
        return self.get_response(request)
