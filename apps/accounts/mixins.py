from django.http import HttpResponseForbidden

class InstructorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Login required")

        if not request.user.is_instructor:
            return HttpResponseForbidden("Instructor access only")

        return super().dispatch(request, *args, **kwargs)
