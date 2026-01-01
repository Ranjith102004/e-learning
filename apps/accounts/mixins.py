from django.http import HttpResponseForbidden


class InstructorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not getattr(request.user, 'is_instructor', False):
            return HttpResponseForbidden("Instructor access only")
        return super().dispatch(request, *args, **kwargs)